from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from website.config import Config
import os


app = Flask(__name__)
# .from_object method tells us we are using those config values from the Config class
app.config.from_object(Config)
db = SQLAlchemy(app)

# import the name of our Blueprint instances
from website.main.routes import main
from website.sort.routes import sort
from website.errors.handlers import errors

# and register the blueprint
app.register_blueprint(main)
app.register_blueprint(sort)
app.register_blueprint(errors)
