from crayfish_analysis_app.models import db, User
from flask import get_flashed_messages
from werkzeug.security import check_password_hash, generate_password_hash


def test_get_home(test_client):
    """
    GIVEN the user goes to the home page
    THEN it should take the user to the home page
        and the status code given should be 200
    """
    response = test_client.get("/home")
    assert response.status_code == 200


def test_get_signup(test_client):
    """
    GIVEN the user goes to the signup page
    THEN it should take the user to the signup page
        and the status code given should be 200
    """
    response = test_client.get("/signup")
    assert response.status_code == 200


def test_get_dashboard(test_client):
    """
    GIVEN the user goes to the dashboard page
    THEN it should take the user to the dashboard app
        and the status code given should be 308
    """
    response = test_client.get("/dashboard")
    assert response.status_code == 308


def test_get_forum(test_client):
    """
    GIVEN the user goes to the forum page
    THEN it should take the user to the forum page
        and the status code given should be 200
    """
    response = test_client.get("/forum")
    assert response.status_code == 200


def test_get_about(test_client):
    """
    GIVEN the user goes to the about page
    THEN it should take the user to the about page
        and the status code given should be 200
    """
    response = test_client.get("/about")
    assert response.status_code == 200


def test_get_database1(test_client):
    """
    GIVEN
    WHEN
    THEN
    """
    response = test_client.get("/crayfish1")
    assert response.status_code == 200


def test_get_database2(test_client):
    """
    GIVEN
    WHEN
    THEN
    """
    response = test_client.get("/crayfish2")
    assert response.status_code == 200


def test_get_login(test_client):
    """
    GIVEN
    WHEN
    THEN
    """
    response = test_client.get("/login")
    assert response.status_code == 200


def test_get_logout(test_client, create_user):
    test_client.post("/login", data={
        "email": "testingsample@test.com",
        "password": "123456",
    })

    response = test_client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    # Check that it is redirected to homepage.
    assert response.request.path == "/home"


def test_post_signup_new_user(test_client):
    # Check if the record exists, it does then delete it
    exists = db.session.execute(
        db.select(User).filter_by(username="crayfish_king")
    ).scalar()
    if exists:
        db.session.execute(db.delete(User).where(User.username == "crayfish_king"))
        db.session.commit()

    response = test_client.post("/signup", data={
        "username": "crayfish_king",
        "email": "crayfish_king@crayfish.com",
        "password1": "ilovecrayfish",
        "password2": "ilovecrayfish"
    })

    target = db.session.execute(
        db.select(User).filter_by(username="crayfish_king")
    ).scalar()

    assert response.status_code == 302
    assert target.email == "crayfish_king@crayfish.com"
    assert check_password_hash(target.password, 'ilovecrayfish') is True


def test_post_signup_invalid_email(test_client):
    # Check if the record exists, it does then delete it
    exists = db.session.execute(
        db.select(User).filter_by(username="Invalid_email")
    ).scalar()
    if exists:
        db.session.execute(db.delete(User).where(User.username == "Invalid_email"))
        db.session.commit()

    test_client.post("/signup", data={
        "username": "Invalid_email",
        "email": "I-am-invalid-email",
        "password1": "invalidemail",
        "password2": "invalidemail"
    })
    text = ''.join(get_flashed_messages())

    assert text == 'Email is invalid.'


def test_post_signup_existing_email(test_client):
    # Check if the record exists, it does then delete it
    exists = db.session.execute(
        db.select(User).filter_by(username="Existing_User")
    ).scalar()
    if not exists:
        exist_user = User(email='existinguser@user.com', username='Existing_User',
                          password=generate_password_hash('existinguser', method='sha256'))
        db.session.add(exist_user)
        db.session.commit()

    test_client.post("/signup", data={
        "username": "username",
        "email": "existinguser@user.com",
        "password1": "existinguser",
        "password2": "existinguser"
    })
    text = ''.join(get_flashed_messages())

    assert text == 'Email is already in use.'


def test_post_signup_existing_user(test_client):
    # Check if the record exists, it does then delete it
    exists = db.session.execute(
        db.select(User).filter_by(username="Existing_User")
    ).scalar()
    if not exists:
        exist_user = User(email='existinguser@user.com', username='Existing_User',
                          password=generate_password_hash('existinguser', method='sha256'))
        db.session.add(exist_user)
        db.session.commit()

    test_client.post("/signup", data={
        "username": "Existing_User",
        "email": "useruser@gmail.com",
        "password1": "existinguser",
        "password2": "existinguser"
    })
    text = ''.join(get_flashed_messages())

    assert text == 'Username is already in use.'


def test_post_signup_not_same_password(test_client):
    exists = db.session.execute(
        db.select(User).filter_by(username="Invalid_email")
    ).scalar()
    if exists:
        db.session.execute(db.delete(User).where(User.username == "Invalid_email"))
        db.session.commit()

    test_client.post("/signup", data={
        "username": "Invalid_email",
        "email": "I-am-invalid-email",
        "password1": "invalidemail",
        "password2": "invalidemail2"
    })
    text = ''.join(get_flashed_messages())

    assert text == "Passwords don't match!"


def test_post_login(test_client, create_user):
    response = test_client.post("/login", data={
        "email": "testingsample@test.com",
        "password": "123456",
    })
    text = ''.join(get_flashed_messages())
    assert response.status_code == 302
    assert text == 'Logged in!'


def test_post_login_wrong_password(test_client, create_user):
    test_client.post("/login", data={
        "email": "testingsample@test.com",
        "password": "WrongPassword",
    })
    text = ''.join(get_flashed_messages())

    assert text == 'Password is incorrect.'


def test_post_login_wrong_email(test_client, create_user):
    test_client.post("/login", data={
        "email": "WrongEmail@test.com",
        "password": "123456",
    })
    text = ''.join(get_flashed_messages())

    assert text == 'Email does not exist.'


def test_post_delete_user(test_client, create_user):
    test_client.post("/login", data={
        "email": "testingsample@test.com",
        "password": "123456",
    })

    target = db.session.execute(
        db.select(User).filter_by(username="IamTest")
    ).scalar()

    target_id = target.id

    response = test_client.post(f"/delete-account/{target_id}")

    exist = db.session.execute(
        db.select(User).filter_by(username="IamTest")
    ).scalar()

    assert response.status_code == 302
    assert exist is None


def test_post_create_forum_without_login(test_client, create_user):
    response = test_client.get("/create-post", follow_redirects=True)

    text = ''.join(get_flashed_messages())
    assert response.status_code == 200
    assert text == 'Please log in to access this page.'
