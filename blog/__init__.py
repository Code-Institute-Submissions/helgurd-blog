import os
import secrets
from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine, Document
from flask_login import LoginManager
import babel

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'blog_two',
    'host': 'mongodb+srv://user:usr2022psswrd@cluster0.m6zch.mongodb.net/blog?retryWrites=true&w=majority'
    # 'host': 'mongodb://localhost:27017'
}

# heroku config:set MONGODB_URI='mongodb+srv://user:usr2022psswrd@cluster0.m6zch.mongodb.net/blog?retryWrites=true&w=majority'

@app.template_filter()
def format_datetime(value, format='medium'):
    if format == 'full':
        format = "EEEE, d. MMMM y 'at' HH:mm"
    elif format == 'medium':
        format = "EE dd.MM.y HH:mm"
    return babel.dates.format_datetime(value, format)


db = MongoEngine(app)
app.config['SECRET_KEY'] = secrets.token_hex()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

UPLOAD_FOLDER = os.getcwd()
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, "static/uploads")

from blog import routes
