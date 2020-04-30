# app/__init__.py
from flask import Flask

class Config(object):
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

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
config_name = 'development'

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    return app
