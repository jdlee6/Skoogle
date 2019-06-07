from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'AAAAA'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///results.db'
db = SQLAlchemy(app)
API_KEY = os.environ.get('API_KEY')
print(API_KEY)

# geolocator = Nominatim(user_agent="myapplication")


from app import routes