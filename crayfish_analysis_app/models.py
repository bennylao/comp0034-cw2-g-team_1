from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_login import LoginManager
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from config import Config

db = SQLAlchemy()


class User(db.Model, UserMixin):
    """User"""

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.Date, nullable=True, default=datetime.utcnow)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    posts = db.relationship('Post', backref='user', passive_deletes=True)
    comments = db.relationship('Comment', backref='user', passive_deletes=True)
    likes = db.relationship('Like', backref='user', passive_deletes=True)


    #Creating a unique token which is valid for 15 minutes
    def get_reset_token(self,expires_sec=900):
        #initializing the serializer with the secret key & expiration time
        serial = Serializer(Config.SECRET_KEY, expires_sec)
        #returns the serialized token with users id as a string
        return serial.dumps({'user_id': self.id}).decode('utf-8')
    
    #Verifying the token 
    @staticmethod
    def verify_token(token):
        serial = Serializer(Config.SECRET_KEY)
        try:
            #deserializing the token and gets the users id
            user_id = serial.loads(token)['user_id']
        except:
            return None
        #finds user object with the given id and returns it 
        return User.query.get(user_id)

    def __repr__(self):
        """
        Returns the attributes of User as a string
        :returns str
        """
        clsname = self.__class__.__name__
        return f"{clsname}: <{self.date_created}, {self.id}, {self.username}, {self.email}, {self.password} >"


login_manager = LoginManager()
login_manager.login_view = "views.login"


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    """Posts made"""

    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.Date, nullable=True, default=datetime.utcnow)
    text = db.Column(db.Text, nullable=False)
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    comments = db.relationship('Comment', backref='post', passive_deletes=True)
    likes = db.relationship('Like', backref='Post', passive_deletes=True)

    def __repr__(self):
        """
        Returns the attributes of Post as a string
        :returns str
        """
        clsname = self.__class__.__name__
        return f"{clsname}: <{self.date_created}, {self.id}, {self.text}, {self.author}>"


class Comment(db.Model):
    """Comments on posts"""

    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.Date, nullable=True, default=datetime.utcnow)
    text = db.Column(db.String(200), nullable=False)
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        """
        Returns the attributes of Comment as a string
        :returns str
        """
        clsname = self.__class__.__name__
        return f"{clsname}: <{self.date_created}, {self.id}, {self.text}, {self.author}, {self.post_id}>"


class Like(db.Model):
    """Likes on post"""

    __tablename__ = "like"
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.Date, nullable=True, default=datetime.utcnow)
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        """
        Returns the attributes of Like as a string
        :returns str
        """
        clsname = self.__class__.__name__
        return f"{clsname}: <{self.date_created}, {self.id}, {self.author}, {self.post_id}>"


class Crayfish1(db.Model):
    """Sheet_1 form prepared_datasets.xlsx"""

    __tablename__ = "crayfish1"
    id = db.Column(db.Integer, primary_key=True)
    site = db.Column(db.String(10), nullable=False)
    method = db.Column(db.String(25), nullable=False)
    gender = db.Column(db.String(2), nullable=False)
    length = db.Column(db.Float, nullable=False)

    def __repr__(self):
        """
        Returns the attributes of Crayfish1 as a string
        :returns str
        """
        clsname = self.__class__.__name__
        return f"{clsname}: < {self.id}, {self.site}, {self.method}, {self.gender}, {self.length}>"


class Crayfish2(db.Model):
    """Sheet_2 form prepared_datasets.xlsx"""

    __tablename__ = "crayfish2"
    id = db.Column(db.Integer, primary_key=True)
    site = db.Column(db.String(10), nullable=False)
    gender = db.Column(db.String(2), nullable=False)
    length = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)

    def __repr__(self):
        """
        Returns the attributes of Crayfish2 as a string
        :returns str
        """
        clsname = self.__class__.__name__
        return f"{clsname}: < {self.id}, {self.site}, {self.gender}, {self.length}, {self.weight}>"
