from flask import Flask


def create_app(config_class_name):
    """Create and configure the Flask app"""
    app = Flask(__name__,template_folder="templates")

    app.config.from_object(config_class_name)

    from crayfish_analysis_app.auth import main_bp
    
    app.register_blueprint(main_bp, url_prefix="/")

    return app
