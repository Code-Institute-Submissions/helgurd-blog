from flask_login import UserMixin
from datetime import datetime
from blog import db


class User(UserMixin, db.Document):
    meta = {'collection': 'user'}
    name = db.StringField(max_length=100)
    username = db.StringField(max_length=30)
    email = db.StringField(max_length=100)
    password = db.StringField()


class Category(UserMixin, db.Document):
    meta = {'collection': 'category'}
    name = db.StringField(max_length=100)


class BlogPost(UserMixin, db.Document):
    meta = {'collection': 'post'}
    title = db.StringField(max_length=100)
    description = db.StringField(max_length=30)
    author = db.StringField(max_length=100)
    image_path = db.StringField(max_length=100)
    created_at = db.DateTimeField(default=datetime.now)
    updated_at = db.DateTimeField(default=datetime.now)
    category = db.StringField(max_length=100)
