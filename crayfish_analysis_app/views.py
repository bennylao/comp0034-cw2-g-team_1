import csv
from io import StringIO
from flask import Blueprint, render_template, request, flash, url_for, redirect, request, make_response, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, db, Post, Comment, Like, Crayfish1, Crayfish2
import re
from crayfish_analysis_app.schemas import Crayfish1Schema, Crayfish2Schema

main_bp = Blueprint('views', __name__)


@main_bp.route('/')
@main_bp.route("/home")
# @login_required
def home():
    """Returns home page """
    posts = Post.query.all()
    return render_template('home.html', user=current_user, posts=posts)


@main_bp.route("/signup", methods=['GET', 'POST'])
def signup():
    """Render signup page and handle signup form submission"""
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # Regular expression for validating an Email
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,4}\b'

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        if email_exists:
            flash('Email is already in use.', category='error')
        elif username_exists:
            flash('Username is already in use.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match!', category='error')
        elif len(username) < 3:
            flash('Username is too short. It must be 3 characters or more.', category='error')
        elif len(password1) < 6:
            flash('Password is too short. It must be 6 characters or more.', category='error')
        elif not re.fullmatch(regex, email):
            flash('Email is invalid.', category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created!')
            return redirect(url_for('views.home'))

    return render_template('signup.html', user=current_user)


@main_bp.route("/login", methods=['GET', 'POST'])
def login():
    """Returns login page"""
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template('login.html', user=current_user)


@main_bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()
        if user:
            flash('A reset link has been sent to this email.', category='success')
        else:
            flash('This email is not recognised.', category='error')

    return render_template('reset_password.html', user=current_user, title='Reset Password')


@main_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))


@main_bp.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')

        if not text:
            flash('Post cannot be empty.', category='error')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.forum'))

    return render_template('create_post.html', user=current_user)


@main_bp.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category="error")
    elif current_user.id != post.user.id:
        flash("You do not have permission to delete this post.", category="error")
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted.", category="success")
    return redirect(url_for('views.forum'))


@main_bp.route("/change-password", methods=['GET', 'POST'])
@login_required
# checks the old password against the existing database password.
# if the old password matches, then the user can change their password using Post method.
def change_password():
    # obtains the entry inputted by the user.
    if request.method == 'POST':
        old_password = request.form.get("old_password")
        new_password1 = request.form.get("new_password1")
        new_password2 = request.form.get("new_password2")

        # checks old password against the database & displays error message if they don't match.
        if not check_password_hash(current_user.password, old_password):
            flash('Old password is incorrect.', category='error')

        # checks if the new passwords are the same.
        elif new_password1 != new_password2:
            flash('New passwords don\'t match!', category='error')

        # checks if length of new password meets the requirement.
        elif len(new_password1) < 6:
            flash('Password is too short. It must be 6 characters or more.', category='error')

        # updates the database with the new password.
        else:
            current_user.password = generate_password_hash(new_password1, method='sha256')
            db.session.commit()
            flash('Password has been successfully changed!', category='success')
            return redirect(url_for('views.home'))

    return render_template('home.html', user=current_user)


@main_bp.route("/delete-account/<id>", methods=['POST'])
@login_required
def delete_user(id):
    user = User.query.filter_by(id=id).first()

    if not user:
        flash("User does not exist.", category="error")
    elif current_user.id != user.id:
        flash("You do not have permission to delete this user.", category="error")
    else:
        # Delete the user's posts
        Post.query.filter_by(author=id).delete()
        # Delete the user's comments
        Comment.query.filter_by(author=id).delete()
        # Delete the user's likes
        Like.query.filter_by(author=id).delete()
        # Delete the user
        db.session.delete(user)
        db.session.commit()
        flash("Account successfully deleted.", category="success")
        return redirect(url_for('views.home'))
    return redirect(url_for('views.home'))


@main_bp.route("/posts/<username>")
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash("No user with that username exists.", category="error")
        return redirect(url_for("views.forum"))

    posts = user.posts
    return render_template("posts.html", user=current_user, posts=posts, username=username)


@main_bp.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash("Comment cannot be empty.", category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
            flash("Comment added.", category="success")

    return redirect(url_for("views.forum"))


@main_bp.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash("Comment does not exist.", category="error")
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash("You do not have permission to delete this comment.", category="error")
    else:
        db.session.delete(comment)
        db.session.commit()
        flash("Comment deleted.", category="success")

    return redirect(url_for("views.forum"))


@main_bp.route("/like-post/<post_id>", methods=["GET"])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id)
    like = Like.query.filter_by(author=current_user.id, post_id=post_id).first()

    if not post:
        flash("Post does not exist.", category="error")
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return redirect(url_for("views.forum"))


@main_bp.route("/about")
def about():
    """Returns about page """
    return render_template('about.html', user=current_user)


@main_bp.route("/account-management")
@login_required
def account_management():
    """Returns account management page """
    return render_template('account_management.html', user=current_user)


@main_bp.route("/forum")
def forum():
    """Returns forum page """
    posts = Post.query.all()
    return render_template('forum.html', user=current_user, posts=posts)


crayfish1s_schema = Crayfish1Schema(many=True)
crayfish1_schema = Crayfish1Schema()
crayfish2s_schema = Crayfish2Schema(many=True)
crayfish2_schema = Crayfish2Schema()


@main_bp.route("/crayfish1")
def crayfish1():
    """Returns a list crayfish data in crayfish1 in JSON."""
    # Select all the regions using Flask-SQLAlchemy
    all_crayfish1 = db.session.execute(db.select(Crayfish1)).scalars()
    # Get the data using Marshmallow schema (returns JSON)
    result = crayfish1s_schema.dump(all_crayfish1)
    # Return the data
    return render_template("crayfish1.html", crayfish_list=result, user=current_user)


@main_bp.get("/crayfish1/<int:id>")
def crayfish1_id(id):
    """Returns the details for a specified id"""
    # Query the database to find the record, return a 404 not found code it the record isn't found
    crayfish = db.session.execute(
        db.select(Crayfish1).filter_by(id=id)
    ).scalar_one_or_none()
    # Get the data using Marshmallow schema (returns JSON) and return the data
    return crayfish1_schema.dump(crayfish)


@main_bp.get("/crayfish2")
def crayfish2():
    """Returns a list of crayfish data in crayfish2 in JSON."""
    # Select all the regions using Flask-SQLAlchemy
    all_crayfish2 = db.session.execute(db.select(Crayfish2)).scalars()
    # Get the data using Marshmallow schema (returns JSON)
    result = crayfish2s_schema.dump(all_crayfish2)
    # Return the data
    return render_template("crayfish2.html", crayfish_list=result, user=current_user)


@main_bp.get("/crayfish2/<int:id>")
def crayfish2_id(id):
    """Returns the details for a specified id"""
    # Query the database to find the record, return a 404 not found code it the record isn't found
    crayfish = db.session.execute(
        db.select(Crayfish2).filter_by(id=id)
    ).scalar_one_or_none()
    # Get the data using Marshmallow schema (returns JSON) and return the data
    return crayfish2_schema.dump(crayfish)


@main_bp.delete('/crayfish1/<code>')
def crayfish1_delete(code):
    """Removes a crayfish1 record from the dataset."""
    # Query the database to find the record, return a 404 not found code it the record isn't found
    crayfish = db.session.execute(
        db.select(Crayfish1).filter_by(id=code)
    ).scalar_one_or_none()
    # Delete the record you found
    db.session.delete(crayfish)
    db.session.commit()
    # Return a JSON HTTP response to let the person know it was deleted
    text = jsonify({"Successfully deleted": crayfish.id})
    response = make_response(text, 200)
    response.headers["Content-type"] = "application/json"
    return response


@main_bp.delete('/crayfish2/<code>')
def crayfish2_delete(code):
    """Removes a crayfish2 record from the dataset."""
    # Query the database to find the record, return a 404 not found code it the record isn't found
    crayfish = db.session.execute(
        db.select(Crayfish2).filter_by(id=code)
    ).scalar_one_or_none()
    # Delete the record you found
    db.session.delete(crayfish)
    db.session.commit()
    # Return a JSON HTTP response to let the person know it was deleted
    text = jsonify({"Successfully deleted": crayfish.id})
    response = make_response(text, 200)
    response.headers["Content-type"] = "application/json"
    return response


@main_bp.post("/crayfish1")
def crayfish1_add():
    """Adds a new crayfish1 record to the dataset."""
    # Get the values of the JSON sent in the request
    site = request.json.get("site", "")
    method = request.json.get("method", "")
    gender = request.json.get("gender", "")
    length = request.json.get("length", "")
    # Create a new Crayfish1 object using the values
    crayfish = Crayfish1(site=site, method=method, gender=gender, length=length)
    # Save the new crayfish to the database
    db.session.add(crayfish)
    db.session.commit()
    # Return a response to the user with the newly added region in JSON format
    result = crayfish1_schema.jsonify(crayfish)
    return result


@main_bp.post("/crayfish2")
def crayfish2_add():
    """Adds a new crayfish2 record to the dataset."""
    # Get the values of the JSON sent in the request
    site = request.json.get("site", "")
    gender = request.json.get("gender", "")
    length = request.json.get("length", "")
    weight = request.json.get("weight", "")
    # Create a new Crayfish2 object using the values
    crayfish = Crayfish2(site=site, gender=gender, length=length, weight=weight)
    # Save the new crayfish to the database
    db.session.add(crayfish)
    db.session.commit()
    # Return a response to the user with the newly added region in JSON format
    result = crayfish2_schema.jsonify(crayfish)
    return result


@main_bp.patch('/crayfish1/<code>')
def crayfish1_update(code):
    """Updates changed fields for the crayfish1 record"""
    # Find the current crayfish1 in the database
    existing_crayfish = db.session.execute(
        db.select(Crayfish1).filter_by(id=code)
    ).scalar_one_or_none()
    # Get the updated details from the json sent in the HTTP patch request
    crayfish_json = request.get_json()
    # Use Marshmallow to update the existing records with the changes in the json
    crayfish1_schema.load(crayfish_json, instance=existing_crayfish, partial=True)
    # Commit the changes to the database
    db.session.commit()
    # Return json showing the updated record
    updated_region = db.session.execute(
        db.select(Crayfish1).filter_by(id=code)
    ).scalar_one_or_none()
    result = crayfish1_schema.jsonify(updated_region)
    return result


@main_bp.patch('/crayfish2/<code>')
def crayfish2_update(code):
    """Updates changed fields for the crayfish2 record"""
    # Find the current crayfish2 in the database
    existing_crayfish = db.session.execute(
        db.select(Crayfish2).filter_by(id=code)
    ).scalar_one_or_none()
    # Get the updated details from the json sent in the HTTP patch request
    crayfish_json = request.get_json()
    # Use Marshmallow to update the existing records with the changes in the json
    crayfish2_schema.load(crayfish_json, instance=existing_crayfish, partial=True)
    # Commit the changes to the database
    db.session.commit()
    # Return json showing the updated record
    updated_region = db.session.execute(
        db.select(Crayfish2).filter_by(id=code)
    ).scalar_one_or_none()
    result = crayfish2_schema.jsonify(updated_region)
    return result


@main_bp.route('/crayfish1/download')
@login_required
def post1():
    si = StringIO()
    # Creating a new csv instance
    cw = csv.writer(si)
    # Get the data from the crayfish1 table
    crayfish_list = Crayfish1.query.all()
    cw.writerow(["id", "site", "method", "gender", "length (mm)"])
    # Add the data to the csv file
    for crayfish in crayfish_list:
        crayfish_ls = [crayfish.id, crayfish.site, crayfish.method, crayfish.gender, crayfish.length]
        cw.writerow(crayfish_ls)
    output = make_response(si.getvalue())
    # Name the file
    output.headers["Content-Disposition"] = "attachment; filename=database1.csv"
    output.headers["Content-type"] = "text/csv"
    return output


@main_bp.route('/crayfish2/download')
@login_required
def post2():
    si = StringIO()
    # Creating a new csv instance
    cw = csv.writer(si)
    # Get the data from the crayfish2 table
    crayfish_list = Crayfish2.query.all()
    cw.writerow(["id", "site", "gender", "length (mm)", "weight (g)"])
    # Add the data to the csv file
    for crayfish in crayfish_list:
        crayfish_ls = [crayfish.id, crayfish.site, crayfish.gender, crayfish.length, crayfish.weight]
        cw.writerow(crayfish_ls)
    # Name the file
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=database2.csv"
    output.headers["Content-type"] = "text/csv"
    return output
