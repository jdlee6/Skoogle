from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


class Config:
    API_KEY = os.environ.get('API_KEY')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'AAAAA'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@35.236.221.100/postgres'
    GPHOTO_URL = 'https://maps.googleapis.com/maps/api/place/photo?'
    PHOTO_HEIGHT = "1000"