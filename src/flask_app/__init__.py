from flask import Flask


def create_app():
    """Create and configure the Flask app"""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = 'QNWmJZSfRkOrOMqjC-XivA'

    # Include the routes from hello.py
    with app.app_context():
        from . import hello

    return app