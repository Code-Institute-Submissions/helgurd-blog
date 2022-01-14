import secrets
from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine, Document
from flask_login import LoginManager

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'blog_two',
    'host': 'mongodb://localhost:27017'
}

db = MongoEngine(app)
app.config['SECRET_KEY'] = secrets.token_hex()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from blog import routes
