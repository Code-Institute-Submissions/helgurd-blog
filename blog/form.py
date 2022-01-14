from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Email, Length, InputRequired, DataRequired
from blog import login_manager
from blog.models import User


@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(max=30)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=2, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), Length(min=2, max=20)])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField('Email or Username', validators=[InputRequired(), Length(max=30)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=2, max=20)])
    submit = SubmitField("Login")
