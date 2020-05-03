from flask_login import current_user
from flask_socketio import send, emit, emit, join_room, leave_room,close_room, rooms, disconnect
from sqlalchemy.orm.attributes import flag_modified

from models import Room,User
from app import socketio,db

@socketio.on('connect',namespace='/game')
def connect_handler():
    if current_user.is_authenticated:
        emit('connection_ack',{'data':'Connected'})
    else:
        return False  # not allowed here

@socketio.on('join', namespace='/game')
def join(message):
    room_name=message['room']
    if current_user.plays_in!=room_name:
        return False
    join_room(room_name)
    room_retrieved=db.session.query(Room).filter_by(name=room_name).first()
    if room_retrieved==None:
        return False
    emit('room_ack',{'data': 'In rooms: ' + room_name})
    emit('player_join',{'username':current_user.username,'team':current_user.team,'spy':current_user.game_master},room=room_name)

@socketio.on('leave', namespace='/game')
def leave(message):
    room_name=message['room']
    if current_user.plays_in!=room_name:
        return False
    room_retrieved=db.session.query(Room).filter_by(name=room_name).first()
    if room_retrieved==None:
        return False
    leave_room(room_name)
    emit('player_left',{'username':current_user.username},room=room_name)


@socketio.on('guess', namespace='/game')
def verify(message):
    word=message['word']
    room_name=message['room']
    hot=True if message['hot']=="hot" else False
    if current_user.plays_in!=room_name:
        return False # Le joueur ne joue pas dans la game
    room_retrieved=db.session.query(Room).filter_by(name=room_name).first()
    # Si on n'a pas pu récupérer de Room, on sort
    if room_retrieved==None:
        return False
    words=room_retrieved.words_list
    # On vérifie que le mot guess n'était pas déjà révélé
    if not words[word]['guessed']:
        if hot:
            words[word]['guessed']=True # le mot devient deviné
            flag_modified(room_retrieved, "words_list") # on notifie la db d'un changement dans un JSON
            word_team=words[word]['team']
            if word_team=="red" or word_team=="blue":
                rem=room_retrieved.decr_remaining_count(word_team)
                room_retrieved.incr_score(word_team)
                emit('update_score',{'blue_score':room_retrieved.blue_score,'red_score':room_retrieved.red_score},room=room_name)
                if rem==0:
                    for w in words.keys():
                        if not words[w]['guessed']:
                            words[w]['guessed']=True
                            emit('reveal',{'word':w,'team':words[w]['team']},room=room_name)
                    room_retrieved.ongoing=False
                    emit('end_game',{'winner':word_team},room=room_name)
            elif word_team=="black":
                for w in words.keys():
                    if not words[w]['guessed']:
                        words[w]['guessed']=True
                        emit('reveal',{'word':w,'team':words[w]['team']},room=room_name)
                room_retrieved.ongoing=False
                emit('end_game',{'winner':word_team},room=room_name)
            db.session.commit()
            emit('reveal',{'word':word,'team':words[word]['team'],'toast':"toasty"},room=room_name)
         
        # On vérifie que l'user est dans la bonne équipe et que cette équipe a encore des guesses
        elif current_user.team==room_retrieved.to_play and room_retrieved.get_remaining_count(current_user.team)>0:
            words_left=0
            words[word]['guessed']=True # le mot devient deviné
            flag_modified(room_retrieved, "words_list") # on notifie la db d'un changement dans un JSON
            word_team=words[word]['team']
            if words[word]['team']==current_user.team: # le mot deviné appartient à la team du joueur courant
                guesses=room_retrieved.decr_remaining_guess()
                words_left=room_retrieved.decr_remaining_count(current_user.team)
                room_retrieved.incr_score(current_user.team)
                emit('update_score',{'blue_score':room_retrieved.blue_score,'red_score':room_retrieved.red_score},room=room_name) #on notifie la room d'une update du score
                if words_left>0:
                    if guesses==0: # si la team courante n'a plus de guess, elle passe son tour
                        room_retrieved.switch_turn()
                        emit('update_turn',{'team_turn':room_retrieved.to_play},room=room_name)
                    
                    else: # sinon on met à jour les guesses restants
                        emit('update_guesses',{'guesses':guesses},room=room_name)
                    
            else: # le mot deviné n'appartient pas à la team jouant
                if words[word]['team']=="grey":
                    words_left=1
                    room_retrieved.switch_turn()
                    emit('update_turn',{'team_turn':room_retrieved.to_play},room=room_name)
                elif  words[word]['team']=="black":
                    words_left=0
                else: # il appartient à l'équipe adverse
                    opp_team = "blue" if current_user.team=="red" else "red"
                    room_retrieved.incr_score(opp_team)
                    room_retrieved.switch_turn()
                    words_left=room_retrieved.decr_remaining_count(opp_team)
                    emit('update_turn',{'team_turn':room_retrieved.to_play},room=room_name)

                    emit('update_score',{'blue_score':room_retrieved.blue_score,'red_score':room_retrieved.red_score},room=room_name)
            if words_left==0:
                for w in words.keys():
                    if not words[w]['guessed']:
                        words[w]['guessed']=True
                        emit('reveal',{'word':w,'team':words[w]['team']},room=room_name)
                room_retrieved.ongoing=False
                emit('end_game',{'winner':word_team},room=room_name)
                
            db.session.commit()
            emit('reveal',{'word':message['word'],'team':words[word]['team'],'toast':'toasty'},room=room_name)
            
        
@socketio.on('reveal_hint',namespace='/game')
def reveal_hint(message):
    room_name=message['room']
    hint_word=message['hint_word']
    guesses=int(message['guesses'])
    if current_user.plays_in!=room_name:
        return False # le joueur ne joue pas dans la room
    
    room_retrieved=db.session.query(Room).filter_by(name=room_name).first()

    if room_retrieved==None: 
        return False # la room n'existe pas
    # Si le joueur courant est bien un spy master et dans la bonne équipe
    if current_user.game_master and current_user.team+"_spy"==room_retrieved.to_play:
        room_retrieved.hint_word=hint_word
        room_retrieved.remaining_guesses=guesses
        room_retrieved.switch_turn()
        db.session.commit()
        emit('update_turn',{'team_turn':room_retrieved.to_play},room=room_name)
        emit('receive_hint',{'hint_word':hint_word,'guesses':guesses},room=room_name)
