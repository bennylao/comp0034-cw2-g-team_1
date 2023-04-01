from flask import Flask
from .models import db, login_manager

def create_app(config_class_name):
    """Create and configure the Flask app"""
    app = Flask(__name__)

    app.config.from_object(config_class_name)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from crayfish_analysis_app.auth import main_bp
    
    app.register_blueprint(main_bp, url_prefix="/")

    db.init_app(app)

    with app.app_context():
        db.create_all()
        print("Database created successfully!")

    login_manager.init_app(app)

    return app