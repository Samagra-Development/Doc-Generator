"""
Create Flask server for googledoc
"""
# app/__init__.py
from flask import Flask

class Config:
    """
    Common configurations
    """

class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False

APP_CONFIG = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
CONFIG_NAME = 'development'

def create_app():
    """
    create server
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(APP_CONFIG[CONFIG_NAME])
    return app
