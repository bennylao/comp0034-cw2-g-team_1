"""Flask config class for the flask_bp app."""
import pathlib


basedir = pathlib.Path(__file__).parent


class Config(object):
    """Base config for all environments"""

    # Never put SECRET_KEY in GitHub for a deployed app!
    SECRET_KEY = "wLFkhRTi1ELlKXFgKb8OKg"

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(basedir.joinpath("data", "database.db"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # Configuring the mail server
    # Using the gmail server using flask-mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'ranaprasen24@gmail.com'
    MAIL_PASSWORD = 'zuvbrfoamcspsvub'


class ProductionConfig(Config):
    """Production config.
    Not currently implemented.
    """

    pass


class DevelopmentConfig(Config):
    """Development environment config"""

    FLASK_ENV = "development"
    DEBUG = True


class TestingConfig(Config):
    """Test environment config"""

    TESTING = True
    SQLALCHEMY_ECHO = True
