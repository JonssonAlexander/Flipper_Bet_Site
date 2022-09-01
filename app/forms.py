from ast import Sub
from tokenize import String
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length 
from app.models import User

class LoginForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired()]) #Vad betyder [DataRequired]?
    password=PasswordField('Password', validators=[DataRequired()])
    remember_me=BooleanField('Remember me')
    submit=SubmitField('Sign in')

class RegistrationForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired()])
    email=StringField('Email', validators=[DataRequired(), Email()]) #Fungerar men kräver att man skriver in en mail med @, annars kan man inte skapa ett konto och den registreras inte i databasen.
    password=PasswordField('Password', validators=[DataRequired ()])
    password2=PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit=SubmitField('Register')
    
    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('This username is taken. Please use another username.')
    
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email is already taken. Please use another email.')