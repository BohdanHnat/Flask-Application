from flask import Flask
from dotenv import load_dotenv
from app.database import db
from app.user.models import *
from app.event.models import *
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

app = Flask('Event Calendar')

jwt = JWTManager(app)

load_dotenv()

app.config.from_pyfile('app/config.py')

db.init_app(app)

migrate = Migrate(app, db)

@app.errorhandler(404)
def page_not_found(error):
    return "<h1>Looks like you're lost</h1>", 404

@app.errorhandler(500)
def internal_server_error(error):
    return '<h1>My bad...</h1>', 500

from app.event import views
from app.main import views
from app.user import views


