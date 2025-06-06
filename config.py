import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'verysecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False