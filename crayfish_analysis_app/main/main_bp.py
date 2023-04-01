from flask import Blueprint, render_template
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
@main_bp.route("/home")
@login_required
def home():
    """Returns home page """
    return render_template("home.html", user=current_user)

# @main_bp.route("/create-post", methods=['GET', 'POST'])
# @login_required
# def create_post():
#     return render_template('create_post.html', user=current_user)

# @main_bp.route('/about', methods=['GET',])
# def about():
#     """Returns about page """
#     return 'Returns about page'

# @main_bp.route('/user/<username>')
# def user(username):
#     """Returns user account page """
#     return f"Returns account page for {username}"