from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_login import LoginManager
from datetime import datetime
from pathlib import Path
import pandas as pd
from .helper_functions import read_excel_multi_index
from sqlalchemy import func, create_engine


db = SQLAlchemy()


class User(db.Model, UserMixin):
    date_created = db.Column(db.Date, nullable=True, default=datetime.utcnow)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    posts = db.relationship('Post', backref='user', passive_deletes=True)
    comments = db.relationship('Comment', backref='user', passive_deletes=True)
    likes = db.relationship('Like', backref='user', passive_deletes=True)


login_manager = LoginManager()
login_manager.login_view = "views.login"


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.Date, nullable=True, default=datetime.utcnow)
    text = db.Column(db.Text, nullable=False)
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    comments = db.relationship('Comment', backref='post', passive_deletes=True)
    likes = db.relationship('Like', backref='Post', passive_deletes=True)


class Comment(db.Model):
    date_created = db.Column(db.Date, nullable=True, default=datetime.utcnow)
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)


class Like(db.Model):
    date_created = db.Column(db.Date, nullable=True, default=datetime.utcnow)
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)


class Crayfish1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site = db.Column(db.String(10), nullable=False)
    method = db.Column(db.String(25), nullable=False)
    gender = db.Column(db.String(2), nullable=False)
    length = db.Column(db.Float, nullable=False)


class Crayfish2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site = db.Column(db.String(10), nullable=False)
    gender = db.Column(db.String(2), nullable=False)
    length = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)


excel = Path(__file__).parent.parent.joinpath("data", "prepared_datasets.xlsx")
crayfishdb1, crayfishdb2 = read_excel_multi_index(excel)
site_list = list(crayfishdb1.columns.get_level_values(0).unique())
site_df1 = []
site_df2 = []
for site in site_list:
    met_1 = crayfishdb1[site, 'Drawdown'].dropna(how='all')
    met_1.insert(0, "Site", [site] * len(met_1.index), True)
    met_1.insert(1, "Method", ["Drawdown"] * len(met_1.index), True)
    met_2 = crayfishdb1[site, 'Handsearch'].dropna(how='all')
    met_2.insert(0, "Site", [site] * len(met_2.index), True)
    met_2.insert(1, "Method", ["Handsearch"] * len(met_2.index), True)
    met_3 = crayfishdb1[site, 'Trapping'].dropna(how='all')
    met_3.insert(0, "Site", [site] * len(met_3.index), True)
    met_3.insert(1, "Method", ["Trapping"] * len(met_3.index), True)
    site_df1.append(pd.concat([met_1, met_2, met_3]))

for site in site_list:
    sitedb = crayfishdb2[site].dropna(how='all')
    sitedb.insert(0, "Site", [site] * len(sitedb.index), True)
    site_df2.append(sitedb)

Sheet_1 = pd.concat(site_df1).reset_index(drop=True)
Sheet_2 = pd.concat(site_df2).reset_index(drop=True)
