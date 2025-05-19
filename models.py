from database import db
from sqlalchemy import Column, Integer, String
import re
from flask import abort
from flask_sqlalchemy import SQLAlchemy
import enum


# db = SQLAlchemy()

class StatusEnum(enum.Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

task_dependencies = db.Table(
    'task_dependencies',
    db.Column('task_id', db.Integer, db.ForeignKey('tasks.id'), primary_key=True),
    db.Column('depends_on_id', db.Integer, db.ForeignKey('tasks.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    tasks = db.relationship('Task', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }

    @staticmethod
    def validate_email(email):
        if "@" not in email:
            raise ValueError("Invalid email format")

    
class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)

    status = db.Column(db.Enum(StatusEnum), default=StatusEnum.TODO, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)

    dependencies = db.relationship(
        'Task', secondary=task_dependencies,
        primaryjoin=id == task_dependencies.c.task_id,
        secondaryjoin=id == task_dependencies.c.depends_on_id,
        backref='dependents'
    )

    def __repr__(self):
        return f"<Task {self.title}>"


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    tasks = db.relationship('Task', backref='project', lazy=True)

    def __repr__(self):
        return f"<Project {self.name}>"
