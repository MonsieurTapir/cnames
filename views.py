from slugify import slugify
from flask import redirect, url_for, request, session, abort,render_template
from flask_login import login_required,login_user,logout_user,current_user
from sqlalchemy import func 
from urllib.parse import urljoin,urlparse
from hashlib import sha224
import random

from models import User,Room,Word
from app import app,login_manager,db


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def shencode(s):
    return sha224(str(s).encode("utf-8")).hexdigest()


@app.errorhandler(400)
def bad_request(e):
    return render_template('400.html',error=str(e),path=request.path), 400    

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).filter_by(id=user_id).first()
        
def redirect_back(endpoint, **values):
    target = request.form['next']
    if not target or not is_safe_url(target):
        target = url_for(endpoint, **values)
    return redirect(target)


def join_game_room(room_name,team,spy):
     room_retrieved=db.session.query(Room).filter_by(name=room_name).first()
     if room_retrieved == None:
        return 1
     else:
        if current_user.plays_in != None and current_user.plays_in != room_name:
            return 2
        elif current_user.plays_in== None:
            current_user.team=team
            current_user.plays_in=room_name
            current_user.game_master=True if spy else False
            db.session.commit()
        return 0 
         
def create_room(room_name,team,spy):
    if current_user.plays_in!=None:
        return 0
    hotseat=True if team=="hotseat" else False
    room_retrieved=db.session.query(Room).filter_by(name=room_name).first()
    if room_retrieved == None:
        words_list=db.session.query(Word).order_by(func.random()).limit(25).all()
        words={}
        i=0
        blue_count=8
        red_count=7
        first="blue"
        if random.randint(0,1)==1:
            blue_count=7
            red_count=8
            first="red"
        for w in words_list:
            team_own="grey"
            if i==0:
                team_own="black"
            elif i<=blue_count:
                team_own="blue"
            elif i<=15:
                team_own="red"
            i+=1
            jsonified={"value": w.value, "team":team_own,"guessed":False}
            words[w.value]=jsonified
        room_retrieved=Room(room_name,words,current_user.id,first+"_spy",red_count,blue_count,hotseat)
        db.session.add(room_retrieved)
        current_user.team=team
        current_user.plays_in=room_name
        current_user.game_master=True if spy else False
        db.session.commit()
        return 2
    else:
        return 1


@app.route('/',methods=["GET","POST"])
def hello():
    if current_user.is_authenticated:
        if request.method=='POST':
            room_name=request.form['roomname']
            room_name=slugify(room_name)
            team=request.form['team']
            spy=request.form.get('spy')
            if request.form['btn']=='create':
                val=create_room(room_name,team,spy)
                if val==2:
                    return redirect(url_for("game_room",
                                     room_name=room_name))
                elif val==1:
                    return render_template("index.html",
                                           err_create="A room named "+room_name+" already exists.",
                                           username=current_user.username,
                                           guest=False,
                                           jump="creation")
                else:
                    return render_template("index.html",
                                           err_create="You are already in game "+current_user.plays_in,
                                           username=current_user.username,
                                           guest=False,
                                           jump="creation")
            elif request.form['btn']=='join':
                val=join_game_room(room_name,team,spy)
                if val==0:
                    return redirect(url_for("game_room",room_name=room_name))
                elif val==1:
                    return render_template("index.html",
                                           err_join="Room "+room_name+" does not exist.",
                                           username=current_user.username,guest=False,
                                           jump="join")
                else:
                    return render_template("index.html",
                                           err_join="You are already in game "+current_user.plays_in,
                                           jump="join")
                    
        else:
            if current_user.plays_in:
                return render_template("index.html",
                                       username=current_user.username,
                                       guest=False,
                                       playing=True,
                                       room_name=current_user.plays_in)
            else:
                return render_template("index.html",
                                       username=current_user.username,
                                       guest=False)
    else:
        return render_template("index.html",guest=True)

    
@app.route("/login", methods=["GET", "POST"])
def login():
    next=request.args.get('next')
    if current_user.is_authenticated:
        return redirect(url_for('hello'))
    else:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            user_retrieved=db.session.query(User).filter_by(email=email).first()
            if user_retrieved==None:
                return render_template("login.html",err="This email is not associated with any account")
            elif shencode(password) == user_retrieved.password:
                login_user(user_retrieved)
                return redirect_back('hello')
            else:
                return render_template("login.html",err="Wrong password")
        else:
            return render_template("login.html",next=next)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    next=request.args.get('next')
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        email=request.form['email']
        if db.session.query(User).filter_by(email=email).first()!=None:
            return render_template("sign_up.html",err="This email is already associated with an account",next=next)
        elif db.session.query(User).filter_by(username=username).first()!=None:
            return render_template("sign_up.html",err="This username is already in use",next=next)
        else:
            res=db.session.query(func.max(User.id)).first()
            new_id=res[0]+1 if res[0]!= None else 0
            user=User(new_id,email,shencode(password),username)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect_back('hello')
    else:
        return render_template("sign_up.html",next=next)
    

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('hello'))

@app.route('/<room_name>')
@login_required
def game_room(room_name):
    room_retrieved=db.session.query(Room).filter_by(name=room_name).first()
    if room_retrieved== None or current_user.plays_in!=room_name: 
        return redirect(url_for("hello")) # la room n'existe pas ou l'user courant n'appartient pas à la room 
    else:
        keys=room_retrieved.words_list.keys()
        keys=sorted(keys)
        spy_turn=True if "spy" in room_retrieved.to_play else False
        if room_retrieved.hotseat:
            return render_template('room_hotseat.html',
                                   name=room_name,
                                   words=room_retrieved.words_list,
                                   keys=keys,
                                   guest=False,
                                   red_score=room_retrieved.red_score,
                                   blue_score=room_retrieved.blue_score,
                                   owner=(room_retrieved.owner==current_user.id),
                                   spy_master=current_user.game_master)
                            
        else:
            return render_template('room.html',
                               name=room_name,
                               words=room_retrieved.words_list,
                               keys=keys,
                               username=current_user.username,
                               spy_master=current_user.game_master,
                               guest=False,
                               players=room_retrieved.players,
                               red_score=room_retrieved.red_score,
                               blue_score=room_retrieved.blue_score,
                               to_play=room_retrieved.to_play,
                               player_team=current_user.team,
                               guesses=room_retrieved.remaining_guesses,
                               hint_word=room_retrieved.hint_word,
                               spy_turn=spy_turn,
                               owner=(room_retrieved.owner==current_user.id)
        )


@app.route("/leave/<room_name>")
@login_required
def leave_game_room(room_name):
        room_retrieved=db.session.query(Room).filter_by(name=room_name).first()
        if room_retrieved!=None:
            if  current_user in room_retrieved.players :
                room_retrieved.players.remove(current_user)
            else:
                return redirect(url_for('hello'))
            current_user.plays_in=None
            current_user.team=None
            current_user.spy=None
            db.session.commit()
        return redirect(url_for('hello'))

    
@app.route('/delete/<room_name>')
@login_required
def delete_room(room_name):
    if current_user.plays_in==room_name:
        room_retrieved=db.session.query(Room).filter_by(name=room_name).first()
        if current_user.id==room_retrieved.owner:
            players=room_retrieved.players
            for p in players:
                p.plays_in=None
                p.team=None
                p.game_master=None
            db.session.delete(room_retrieved)
            db.session.commit()
            return redirect(url_for("hello"))
        else:
            return redirect(url_for(game_room,room_name=room_name))
    else:
        return redirect(url_for("hello"))


@app.template_filter('team_value')
def get_team_value(x):
    return x.split("_")[0]
    
@app.template_filter('get_value')
def get_word_value(x):
    return x["value"]
@app.template_filter('get_team')
def get_word_team(x):
    return x["team"]
