from flask import Blueprint, render_template
from flask import current_app as app


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/help', methods=['GET',])
def help():
    """Returns help page """
    return 'Returns help page'

