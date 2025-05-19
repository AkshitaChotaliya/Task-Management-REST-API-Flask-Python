import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 'postgresql://postgres:12345@localhost:5432/flask_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False