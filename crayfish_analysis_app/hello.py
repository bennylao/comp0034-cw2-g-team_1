from flask import Blueprint, render_template
from flask import current_app as app


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Returns home page """
    return render_template('index.html')

@main_bp.route('/help', methods=['GET',])
def help():
    """Returns help page """
    return 'Returns help page'

@main_bp.route('/about', methods=['GET',])
def about():
    """Returns about page """
    return 'Returns about page'

@main_bp.route('/forum', methods=['GET',])
def forum():
    """Returns forum page"""
    return 'Returns forum page'

@main_bp.route('/user/<username>')
def user(username):
    """Returns user account page """
    return f"Returns account page for {username}"