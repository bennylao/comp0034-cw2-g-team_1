"""Flask config class for the flask_bp app."""

import os
import pathlib

basedir = os.path.abspath(os.path.dirname(__file__))
basedir_pathlib = pathlib.Path(__file__).parent


class Config(object):
    """Base config for all environments"""

    # Never put SECRET_KEY in GitHub for a deployed app!
    SECRET_KEY = "wLFkhRTi1ELlKXFgKb8OKg"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """Production environment config"""

    pass


class DevelopmentConfig(Config):
    """Development environment config"""

    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    """Test environment config"""

    TESTING = True
    SQLALCHEMY_ECHO = True
