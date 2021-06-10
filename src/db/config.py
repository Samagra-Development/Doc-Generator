"""
Define Database Configuration
"""
class Config:
    """
    Common configurations
    """
    SQLALCHEMY_DATABASE_URI = 'postgresql://pdfbuilder:FKQMoXB7BQyU1zp59DGu@localhost:5423/pdfbuilder'
    SQLALCHEMY_BINDS = {
        'backup': 'postgresql://pdfbuilderbackup:FKQMoXB7BQyU1zp59DGu@localhost:5422/pdfbuilderbackup'
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'p9Bv<3Eid9dQW#$&sdER25wSF2w4fs$i01'  # Secret API key
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
