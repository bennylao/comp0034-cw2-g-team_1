import csv
from io import StringIO
from flask import Blueprint, render_template, flash, url_for, redirect, request, make_response, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, db, Post, Comment, Like, Crayfish1, Crayfish2
import re
from flask_mail import Message
from config import Config
from crayfish_analysis_app.schemas import Crayfish1Schema, Crayfish2Schema

main_bp = Blueprint('views', __name__)


@main_bp.route('/')
@main_bp.route("/home")
# @login_required
def home():
    """
    Redirects to the gome page
    Args:
        
    Raises:
        NA
    Returns:
        home.html page
    """
    return render_template('home.html', user=current_user, posts=posts)


@main_bp.route("/signup", methods=['GET', 'POST'])
def signup():
    """
    This function renders the signup page and creates a new user
    Args:
        NA
    Raises:
        Flask Validation Error(str): If the form is not filled out correctly
        
    Returns:
        The 'home.html' page if singup is successful
        The 'signup.html' page if signup is unsuccessful
    """
    if request.method == 'POST':
        # obtains the entry inputted by the user
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # Regular expression for validating an Email
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,4}\b'

        # finding the email or username in database
        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        # Validating the inputs from form
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
            # if all the validations are passed, then the user is created and added to database
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created!')
            return redirect(url_for('views.home'))

    return render_template('signup.html', user=current_user)


@main_bp.route("/login", methods=['GET', 'POST'])
def login():
    """
    renders the login page and logs in the user
    Args:
        
    Raises:
        Flask Validation Error(str): If the form is not filled out correctly
    Returns:
        The 'home.html' page if login is successful
        The 'login.html' page if login is unsuccessful due to incrrect password or email
    """
    if request.method == 'POST':
        # obtains the entry inputted by the user
        email = request.form.get("email")
        password = request.form.get("password")

        # finding the email in database
        user = User.query.filter_by(email=email).first()

        # validating the inputs from form
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


def send_email(user):
    """
    This function sends the email with reset link to user
    Args: 
        (User Object): The users email address  
    Raises:
        NA
    Returns:
        NA
    """

    # generate reset token using the function get_reset_token() in models.py
    token = user.get_reset_token()
    # creating message object with subject, sender and recipient
    msg = Message('Password Reset Request',
                  sender='ranaprasen24@gmail.com',
                  recipients=[user.email])
    # Message with the reset link with the token
    msg.body = f'''Please click on the link below to reset your password:
{url_for('views.reset_token', token=token, _external=True)}
If you did not request to change password, you can ignore this email.
'''
    # sends the mail through the server set up in __init__.py
    Config.MAIL.send(msg)


@main_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_request():
    """
    This function manages the password reset request and sends the email to the user with the reset link
    Args:
        NA
    Raises:
        Flask Validation Error(str): If the form is not filled out correctly
    Returns:
        The 'login.html' page if email is found & rest link is sent
        The 'reset_request.html' page if email is not found or invalid
    """

    if request.method == 'POST':
        # obtains the entry inputted by the user
        email = request.form.get("email")
        # finds user with the email
        user = User.query.filter_by(email=email).first()
        if user:
            # sends email to the user if email is found
            send_email(user)
            flash('A reset link has been sent to this email.', category='suceess')
            return redirect(url_for('views.login'))
        else:
            flash('This email is not recognised.', category='error')

    return render_template('reset_request.html', user=current_user)


@main_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    """
    This function imports the newly created Excel file in the correct format
    Args:
        token(str): The token generated by the function get_reset_token() in models.py

    Raises:
        Flask ValidationError(str): If the form is not filled out correctly
    Returns:
        The 'reset_token.html' page if token is valid
        The 'reset_request.html' page if token is invalid or expired
    """
    # verifies the token using function verify_token() in models.py
    user = User.verify_token(token)

    if user is None:
        flash('The Token is Expired or Invalid', category='warning')
        return redirect(url_for('views.reset_request'))
    else:
        # obtains entry inputted by the user
        if request.method == 'POST':
            reset_password1 = request.form.get("reset_password1")
            reset_password2 = request.form.get("reset_password2")
            # checks if passwords match and if password is long enough
            if reset_password1 != reset_password2:
                flash('New passwords don\'t match!', category='error')
            elif len(reset_password1) < 6:
                flash('Password is too short. It must be 6 characters or more.', category='error')
            # updates database with new password
            else:
                user.password = generate_password_hash(reset_password1, method='sha256')
                db.session.commit()
                flash('Password has been updated!', category='success')
                return redirect(url_for('views.home'))
    return render_template('reset_token.html', user=current_user)


@main_bp.route("/logout")
@login_required
def logout():
    """
    Logs out the user
    Args:
        NA
    Raises:
        NA
    Returns:
        The 'home.html' page if token is valid

    """
    logout_user()
    return redirect(url_for('views.home'))


@main_bp.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    """
    Creates a post
    Args:
        NA
    Raises:
        flask Validation Error(str): If the form is not filled out correctly
    Returns:
        The 'forum.html' with the new post if the form is filled out correctly
        The 'create_post.html' page if the form is not filled out correctly
    """
    if request.method == "POST":

        # obtains entry inputted by the user
        text = request.form.get('text')

        # validates the input
        if not text:
            flash('Post cannot be empty.', category='error')
        else:

            # creates a new post and updates the database
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.forum'))

    return render_template('create_post.html', user=current_user)


@main_bp.route("/delete-post/<id>")
@login_required
def delete_post(id):
    """
    Deletes a post
    Args:
        id(int): The id of the post
    Raises:
        NA
    Returns:
        The 'forum.html'page with the post deleted

    """
    # obtains the post with the id from the database
    post = Post.query.filter_by(id=id).first()

    # checks if the post exists and if the user has permission to delete the post
    if not post:
        flash("Post does not exist.", category="error")
    elif current_user.id != post.user.id:
        flash("You do not have permission to delete this post.", category="error")
    else:

        # deletes the post and updates the database
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted.", category="success")
    return redirect(url_for('views.forum'))


@main_bp.route("/change-password", methods=['GET', 'POST'])
@login_required
def change_password():
    """
    This funciton changes the password of the user. Checks the old password
    against the existing database password. if the old password matches,
    then the user can change their password using Post method.

    Args:
        NA
    Raises:
        flask Validation Error(str): If the form is not filled out correctly
    Returns:
        The 'home.html' page if the form is filled out correctly
        The 'change_password.html' page if the form is not filled out correctly
    """
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

    return render_template('account_management.html', user=current_user)


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
    """
    This function renders the about page
    Args:
        NA
    Raises:
        NA
    Returns:
        about.html
    """
    return render_template('about.html', user=current_user)


@main_bp.route("/account-management")
@login_required
def account_management():
    """
    This function renders the account management page
    Args:
        NA
    Raises:
        NA
    Returns:
        account_management.html
    """
    return render_template('account_management.html', user=current_user)


@main_bp.route("/forum")
def forum():
    """
    This function renders the forum page
    Args:
        NA
    Raises:
        NA
    Returns:
        forum.html
    """
    # Needs to get all posts from the post model
    posts = Post.query.all()
    return render_template('forum.html', user=current_user, posts=posts)


crayfish1s_schema = Crayfish1Schema(many=True)
crayfish1_schema = Crayfish1Schema()
crayfish2s_schema = Crayfish2Schema(many=True)
crayfish2_schema = Crayfish2Schema()


@main_bp.route("/crayfish1")
def crayfish1():
    """
    This function renders the crayfish1 page
    Args:
        NA
    Raises:
        NA
    Returns:
        crayfish1.html
    """
    # Select all the regions using Flask-SQLAlchemy
    all_crayfish1 = db.session.execute(db.select(Crayfish1)).scalars()
    # Get the data using Marshmallow schema (returns JSON)
    result = crayfish1s_schema.dump(all_crayfish1)
    # Return a list crayfish data in crayfish1 in JSON
    return render_template("crayfish1.html", crayfish_list=result, user=current_user)


@main_bp.get("/crayfish1/<int:id>")
def crayfish1_id(id):
    """
    This function returns the details for a specified id
    Args:
        id
    Raises:
        NA
    Returns:
        crayfish1_schema.dump(crayfish)
    """
    # Query the database to find the record, return a 404 not found code it the record isn't found
    crayfish = db.session.execute(
        db.select(Crayfish1).filter_by(id=id)
    ).scalar_one_or_none()
    # Get the data using Marshmallow schema (returns JSON) and return the data
    return crayfish1_schema.dump(crayfish)


@main_bp.get("/crayfish2")
def crayfish2():
    """
    This function renders the crayfish2 page
    Args:
        NA
    Raises:
        NA
    Returns:
        crayfish2.html
    """
    # Select all the regions using Flask-SQLAlchemy
    all_crayfish2 = db.session.execute(db.select(Crayfish2)).scalars()
    # Get the data using Marshmallow schema (returns JSON)
    result = crayfish2s_schema.dump(all_crayfish2)
    # Return a list of crayfish data in crayfish2 in JSON
    return render_template("crayfish2.html", crayfish_list=result, user=current_user)


@main_bp.get("/crayfish2/<int:id>")
def crayfish2_id(id):
    """
    This function returns the details for a specified id
    Args:
        id
    Raises:
        NA
    Returns:
        crayfish2_schema.dump(crayfish)
    """
    # Query the database to find the record, return a 404 not found code it the record isn't found
    crayfish = db.session.execute(
        db.select(Crayfish2).filter_by(id=id)
    ).scalar_one_or_none()
    # Get the data using Marshmallow schema (returns JSON) and return the data
    return crayfish2_schema.dump(crayfish)


@main_bp.delete('/crayfish1/<code>')
def crayfish1_delete(code):
    """
    This function removes a crayfish1 record from the dataset
    Args:
        code
    Raises:
        NA
    Returns:
        JSON HTTP response
    """
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
    """
    This function removes a crayfish2 record from the dataset
    Args:
        code
    Raises:
        NA
    Returns:
        JSON HTTP response
    """
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
    """
    This function adds a new crayfish1 record to the dataset
    Args:
        NA
    Raises:
        NA
    Returns:
        HTTP response
    """
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
    """
    This function adds a new crayfish2 record to the dataset
    Args:
        NA
    Raises:
        NA
    Returns:
        HTTP response
    """
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
    """
    This function updates changed fields for the crayfish1 record
    Args:
        code
    Raises:
        NA
    Returns:
        JSON result
    """
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
    """
    This function updates changed fields for the crayfish2 record
    Args:
        code
    Raises:
        NA
    Returns:
        JSON result
    """
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
def post1():
    """
    This function generates a CSV file containing data from the crayfish1 table and returns it as a response
    Args:
        NA
    Raises:
        NA
    Returns:
        Flask response object containing the CSV data
    """
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
def post2():
    """
    This function generates a CSV file containing data from the crayfish2 table and returns it as a response
    Args:
        NA
    Raises:
        NA
    Returns:
        Flask response object containing the CSV data
    """
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
