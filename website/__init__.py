from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from website.config import Config
import os


db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    with app.app_context():
        app.config.from_object(Config)
        db.init_app(app)    

        from website.main.routes import main
        from website.sort.routes import sort
        from website.errors.handlers import errors
        app.register_blueprint(main)
        app.register_blueprint(sort)
        app.register_blueprint(errors)

        return app