import pytest
from app import create_app
from app.db import db
from flask.signals import request_finished
from dotenv import load_dotenv
import os
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime

load_dotenv()

@pytest.fixture
def app():
    
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')
    }
    app = create_app(test_config)

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

  
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def one_task(app):
    new_task = Task(title="Go on my daily walk 🏞", 
                    description="Notice something new every day", 
                    completed_at=None)
    db.session.add(new_task)
    db.session.commit()

@pytest.fixture
def three_tasks(app):
    db.session.add_all([
        Task(title="Water the garden 🌷", 
            description="", 
            completed_at=None),
        Task(title="Answer forgotten email 📧", 
            description="", 
            completed_at=None),
        Task(title="Pay my outstanding tickets 😭", 
            description="", 
            completed_at=None)
    ])
    db.session.commit()

@pytest.fixture
def completed_task(app):
    new_task = Task(title="Go on my daily walk 🏞", 
                    description="Notice something new every day", 
                    completed_at=datetime.now())
    db.session.add(new_task)
    db.session.commit()


@pytest.fixture
def one_goal(app):
    new_goal = Goal(title="Build a habit of going outside daily")
    db.session.add(new_goal)
    db.session.commit()

@pytest.fixture
def one_task_belongs_to_one_goal(app, one_goal, one_task):
    task_query = db.select(Task).where(Task.id == 1)
    goal_query = db.select(Goal).where(Goal.id == 1)
    task = db.session.scalar(task_query)
    goal = db.session.scalar(goal_query)
    goal.tasks.append(task)
    db.session.commit()