from flask import Flask
from .models import db, login_manager, Sheet_1, Sheet_2, Crayfish1, Crayfish2
from sqlalchemy import create_engine


def create_app(config_class_name):
    """Create and configure the Flask app"""
    app = Flask(__name__)

    app.config.from_object(config_class_name)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from crayfish_analysis_app.views import main_bp

    app.register_blueprint(main_bp, url_prefix="/")

    db.init_app(app)

    with app.app_context():
        db.create_all()
        print("Database created successfully!")

        #Deletes the crayfish1 and crayfish 2 table
        crayfishTable1 = Crayfish1.query.all()
        crayfishTable2 = Crayfish2.query.all()
        for c in crayfishTable1:
            db.session.delete(c)
        for c in crayfishTable2:
            db.session.delete(c)
        
        #Creates crayfish1 table
        for i in range (len(Sheet_1.index)):
            id = i
            site = Sheet_1.iloc[i].tolist()[0]
            method = Sheet_1.iloc[i].tolist()[1]
            gender = Sheet_1.iloc[i].tolist()[2]
            length = Sheet_1.iloc[i].tolist()[3]
            new_entry = Crayfish1(id = id, site = site, method = method, gender = gender, length = length)
            db.session.add(new_entry)

        #Creates crayfish1 table
        for i in range (len(Sheet_2.index)):
            id = i
            site = Sheet_2.iloc[i].tolist()[0]
            gender = Sheet_2.iloc[i].tolist()[1]
            length = Sheet_2.iloc[i].tolist()[2]
            weight = Sheet_2.iloc[i].tolist()[3]
            new_entry = Crayfish2(id = id, site = site, gender = gender, length = length, weight = weight)
            db.session.add(new_entry)
        
        db.session.commit()

    login_manager.init_app(app)

    return app
