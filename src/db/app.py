# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import *

# db variable initialization
db = SQLAlchemy()

config_name = 'production'

def create_app():
    app = Flask('App', instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    db.init_app(app)
    migrate = Migrate(app, db)
    from .models import pdfData,outputTable
    return app
def get_db():
    app = Flask('App', instance_relative_config=True)
    with app.app_context():
        app.config.from_object(app_config[config_name])
        db.init_app(app)
    
        
    return app  