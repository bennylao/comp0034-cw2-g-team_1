from flask import current_app as app, render_template


# app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")