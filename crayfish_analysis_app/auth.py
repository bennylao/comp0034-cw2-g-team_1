from flask import Blueprint, render_template, request
from .models import User, db

main_bp = Blueprint('auth', __name__)

@main_bp.route('/')
@main_bp.route("/home")
def home():
    """Returns home page """
    return render_template('home.html')

@main_bp.route("/signup", methods=['GET','POST'])
def signup():
    """Render signup page and handle signup form submission"""
    email = request.form.get("email")
    username = request.form.get("username")
    password1 = request.form.get("password1")
    password2 = request.form.get("password2")
    # user = User(email=email, username=username, password=password1)
    # db.session.add(user)
    # db.session.commit()
    return render_template('signup.html')

@main_bp.route("/login", methods=['GET','POST'])
def login():
    """Returns login page"""
    email = request.form.get("email")
    password = request.form.get("password")
    return render_template('login.html')

# @main_bp.route('/about', methods=['GET',])
# def about():
#     """Returns about page """
#     return 'Returns about page'

# @main_bp.route('/user/<username>')
# def user(username):
#     """Returns user account page """
#     return f"Returns account page for {username}"