from flask import Flask
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from dotenv import load_dotenv
from flask_pymongo import PyMongo
import os
import secrets

load_dotenv()


db_pass = os.getenv('DBPASS')
db_user = os.getenv("DBUSER")
db_host = os.getenv("DBHOST")
database = os.getenv("DB")


app = Flask(__name__)
mongo = PyMongo(app)
home = app.instance_path
app.config["SECRET_KEY"] = secrets.token_hex()
app.config["MONGO_URI"] = f"mongodb://localhost:27017/{database}"

ma = Marshmallow(app)

# init bcrypt
bcrypt = Bcrypt(app)

# init the login manager
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from blog import routes
