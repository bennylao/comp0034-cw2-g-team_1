"""Flask config class."""


class Config(object):
    pass


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    TESTING = True
    SECRET_KEY = 'QNWmJZSfRkOrOMqjC-XivA'


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = 'QNWmJZSfRkOrOMqjC-XivA'
