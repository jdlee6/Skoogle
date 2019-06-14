from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'AAAAA'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@35.226.56.130/postgres'
db = SQLAlchemy(app)
API_KEY = os.environ.get('API_KEY')
# print(API_KEY)


from app import routes