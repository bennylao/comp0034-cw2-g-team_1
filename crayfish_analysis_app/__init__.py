from flask import Flask
from .models import db, login_manager
from flask_marshmallow import Marshmallow
from .dash_app.app import create_dash_app
from flask_mail import Mail
from config import Config

# Create a global Flask-Marshmallow object
ma = Marshmallow()


def create_app(config_class_name):
    """Create and configure the Flask app"""

    global mail

    app = Flask(__name__)

    app.config.from_object(config_class_name)

    from crayfish_analysis_app.views import main_bp

    app.register_blueprint(main_bp, url_prefix="/")

    db.init_app(app)
    ma.init_app(app)

    create_dash_app(app)

    with app.app_context():

        db.create_all()
        print("Database created successfully!")

    login_manager.init_app(app)

     #Configuring the mail server
    #Using the gmail server using flask-mail
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'ranaprasen24@gmail.com'
    app.config['MAIL_PASSWORD'] = 'zuvbrfoamcspsvub'
    #initialising the extension with flask app
    mail = Mail(app)

    Config.MAIL = mail

    return app
