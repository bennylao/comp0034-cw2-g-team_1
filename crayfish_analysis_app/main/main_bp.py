from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
@main_bp.route("/home")
def home():
    """Returns home page """
    return render_template("home.html")