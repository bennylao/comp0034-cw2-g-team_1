from flask import Blueprint, render_template

main_bp = Blueprint('auth', __name__)

@main_bp.route('/')
@main_bp.route('/home')
def home():
    """Returns home page """
    return render_template('home.html')

@main_bp.route('/signup')
def signup():
    """Returns signup page """
    return render_template('signup.html')

@main_bp.route('/login')
def login():
    """Returns login page"""
    return render_template('login.html')

# @main_bp.route('/about', methods=['GET',])
# def about():
#     """Returns about page """
#     return 'Returns about page'

# @main_bp.route('/user/<username>')
# def user(username):
#     """Returns user account page """
#     return f"Returns account page for {username}"