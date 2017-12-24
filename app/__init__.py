from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_htmlmin import HTMLMIN

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

HTMLMIN(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)

bootstrap = Bootstrap(app)

from app import models, errors, routes
