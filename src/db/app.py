"""
Create Flask Application and Initialize Database
"""

# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import *

# db variable initialization
DB = SQLAlchemy()

CONFIG_NAME = 'production'

def create_app():
    """
    create flask application and initialize database
    """
    app = Flask('App', instance_relative_config=True)
    app.config.from_object(APP_CONFIG[CONFIG_NAME])
    DB.init_app(app)
    migrate = Migrate(app, DB)
    from .models import PdfData, OutputTable
    return app
def get_db():
    """
    create flask application and get database
    """
    app = Flask('App', instance_relative_config=True)
    with app.app_context():
        app.config.from_object(APP_CONFIG[CONFIG_NAME])
        DB.init_app(app)
    return app
