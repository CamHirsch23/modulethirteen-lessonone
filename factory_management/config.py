import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///factory_management.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False