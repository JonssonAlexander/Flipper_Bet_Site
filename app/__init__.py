from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

app= Flask(__name__)
app.config.from_object(Config)
db=SQLAlchemy(app)
migrate = Migrate(app, db)
login=LoginManager(app)
login.login_view='login' #Gör att vissa sidor under koden @login_required inte kan nås utan att logga in. Då måste dock flask_login import login_required importeras. 
mail=Mail(app)
from app import routes, models