from flask_login import UserMixin

from blog import db


class User(UserMixin, db.Document):
    meta = {'collection': 'user'}
    username = db.StringField(max_length=30)
    email = db.StringField(max_length=100)
    password = db.StringField()
