from flask import Flask
from .db import db, migrate
from .routes.task_routes import tasks_bp
from .routes.goal_routes import goals_bp 
from .models import task, goal
import os

def create_app(config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(tasks_bp, url_prefix="/tasks")
    app.register_blueprint(goals_bp, url_prefix="/goals")
    return app
