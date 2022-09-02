from app import db
from datetime import datetime 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5
from time import time

class User(UserMixin, db.Model): 
    id= db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(64), index=True, unique=True)
    email= db.Column(db.String(120), index=True, unique=True)
    password_hash= db.Column(db.String(128))
    about_me= db.Column(db.String(180))
    maxscore=db.Column(db.String(180)) #OBS! Gjorde den som en string och inte som en integer, kan bli bökigt sen när vi inför elo
    wins= db.Column(db.Integer,index=True)
    losses=db.Column(db.Integer,index=True)
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash=generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Game(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    player1= db.Column(db.String(64))
    player2= db.Column(db.String(64))
    bets=db.Column(db.String(180))
    odds=db.Column(db.String(50),index=True)
    available=db.Column(db.Boolean, default=False)
    #ev lägg till timestamp

    def __repr__(self):
        return '<Game {}>'.format(self.body)
    


