from flask import Flask, render_template, request, url_for, flash, redirect
from app import app 
from app.forms import LoginForm 
from app.forms import RegistrationForm
from app.forms import MatchForm
from flask_login import current_user, login_user
from app.models import User
from app.models import Game
from flask_login import logout_user
from flask_login import login_required
from werkzeug.urls import url_parse
from app import db
import random 

be = Flask(__name__, static_folder='static')


Games = {
    "players": ["Alex vs Benji"]*10,
    "times": ["18:00:00"]*10,
    "results": [(102390, 203300)]*10,
    "comments": ["Semifinal mellan åttan och sextionian"]*10,
    "ids": range(10)
}
bets = {
    "players": [('Anders', 'Jonas')]*10,
    "insättning": ['🍻x1']*10,
    "odds": ['2:1']*10,
    "played": [True, False, False, True, False, False, True, True, True, True],
    "positions": [(random.randint(1, 5), random.randint(1, 8)) for i in range(10)],
    "ids": range(10)
}



#def index():
  #  return render_template('index.html', players=Games['players'], times=Games['times'], results=Games['results'], comments=Games["comments"], nr_of_games=len(Games['players']))

@app.route('/', methods=('GET', 'POST'))
def index():
    classes = ["mlb" if x else 'pga' for x in bets['played']]
    games=Game.query.all()
    return render_template('index.html', games=games, classes=classes, players=Games['players'], times=Games['times'], results=Games['results'], comments=Games["comments"], ids=Games["ids"], nr_of_games=len(Games['players']))

@app.route('/bettingpage', methods=('GET', 'POST'))

def betting():
    games=Game.query.all()
    
    return render_template('index.html', games=games, players=Games['players'], times=Games['times'], results=Games['results'], comments=Games["comments"], nr_of_games=len(Games['players']))

@app.route('/login', methods= ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=LoginForm()
    if form.validate_on_submit():
        user =User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page= request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page=url_for('index')
        return redirect(next_page)
    return render_template('login.html', title= 'Sign in', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index')) 

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)



@app.route('/<match_id>', methods=('GET', 'POST'))
def matchestype(match_id):

    classes = ["mlb" if x else 'pga' for x in bets['played']]

    return render_template('bets.html', ids=["ids"], insättning=bets["insättning"], classes=classes, players=bets['players'], odds=bets['odds'], played=bets['played'], nr_of_bets=len(bets['players']), positions=bets['positions'])

@app.route('/match', methods= ['GET', 'POST'])
@login_required
def match():
    form=MatchForm()
    if form.validate_on_submit():
        game = Game(player1=form.player1.data, player2=form.player2.data, odds=form.odds.data, bets=form.bets.data, available=form.available.data )
        db.session.add(game)
        db.session.commit()
        flash('Your match-request is now public')
        return redirect(url_for('index'))
    return render_template('post_match.html', title='Match', form=form)
   
    #skicka till en annan sida, där säger den "är du säker?" Om du skriver ja uppdateras game.played till true och du skickas till 
    #ytterligare en sida där du ska skriva in vem som vann för att uppdatera game.losses/game.wins

#@app.route('/match_confirm', methods= ['GET', 'POST'])
#@login_required
#def confirm_match():
    #form=MatchForm()
    #if form.validate_on_submit():
        #game = Game.query.filter_by(match=) #problem, hur identifierar man matcherna
        #game.available = Game(form.available.data)
        #db.session.commit()



        