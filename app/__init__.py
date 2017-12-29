from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_htmlmin import HTMLMIN
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

__all__ = ['app', 'db', 'migrate', 'forms', 'models', 'routes']

app = Flask(__name__)
app.config.from_object(Config)

HTMLMIN(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)

bootstrap = Bootstrap(app)

# Allows migrate to work
# noinspection PyUnresolvedReferences
from .models import *
# noinspection PyUnresolvedReferences
from .routes import *
