from app import db
from sqlalchemy.dialects.postgresql import JSON
from flask_login import UserMixin

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id= db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String())
    password=db.Column(db.String())
    username=db.Column(db.String())
    plays_in = db.Column(db.String(), db.ForeignKey('rooms.name'))
    game_master=db.Column(db.Boolean)
    team=db.Column(db.String())
    def __init__(self,id,  email, password,username):
        self.id = id
        self.email = email
        self.password = password
        self.username=username
        self.plays_in=None
    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.username, self.email)

class Word(db.Model):
    __tablename__ = 'words'
    id=db.Column(db.Integer,primary_key=True)
    value=db.Column(db.String())
    def __init__(self,id,value):
        self.id=id
        self.value=value
    def __repr__(self):
        return "%d/%s" % (self.id, self.value)

class Room(db.Model):
    __tablename__= 'rooms'
    name=db.Column(db.String(),primary_key=True)
    words_list=db.Column(db.JSON)
    owner=db.Column(db.Integer())
    red_score=db.Column(db.Integer())
    blue_score=db.Column(db.Integer())
    blue_to_guess=db.Column(db.Integer())
    red_to_guess=db.Column(db.Integer())
    remaining_guesses=db.Column(db.Integer())
    hint_word=db.Column(db.String())
    to_play=db.Column(db.String())
    ongoing=db.Column(db.Boolean)
    hotseat=db.Column(db.Boolean)
    players=db.relationship(User, backref='room', lazy=True)
    def __init__(self,name,words,owner,to_play,red_to,blue_to,hotseat):
        self.name=name
        self.words_list=words
        self.owner=owner
        self.players=[]
        self.red_score=0
        self.blue_score=0
        self.to_play=to_play
        self.red_to_guess=red_to
        self.blue_to_guess=blue_to
        self.ongoing=True
        self.hotseat=hotseat
    def incr_score(self,team):
        if team=="red":
            self.red_score+=1
        else:
            self.blue_score+=1
    def switch_turn(self):
        if self.to_play=="red":
            self.to_play="blue_spy"
        elif self.to_play=="red_spy":
            self.to_play="red"
        elif self.to_play=="blue":
            self.to_play="red_spy"
        else:
            self.to_play="blue";

    def decr_remaining_guess(self):
        self.remaining_guesses-=1
        return self.remaining_guesses
        
    def get_remaining_count(self,team):
         if team=="red":
            return self.red_to_guess
         else:
            return self.blue_to_guess
        
    def decr_remaining_count(self,team):
         if team=="red":
            self.red_to_guess -= 1
            return self.red_to_guess
         else:
            self.blue_to_guess -=1
            return self.blue_to_guess
    def incr_score(self,team):
        if team=="red":
            self.red_score += 1
            return self.red_score
        else:
            self.blue_score +=1
            return self.blue_score
