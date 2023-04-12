from crayfish_analysis_app.models import db
from crayfish_analysis_app.models import User
from flask import get_flashed_messages, url_for, request
from werkzeug.security import check_password_hash


def test_get_home(test_client):
    """
    GIVEN
    WHEN
    THEN
    """
    response = test_client.get("/home")
    assert response.status_code == 200


def test_get_signup(test_client):
    """
    GIVEN
    WHEN
    THEN
    """
    response = test_client.get("/signup")
    assert response.status_code == 200


def test_post_signup_new_user(test_client):
    # Check if the region exists, it does then delete it
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


def test_get_logout(test_client, create_user):
    test_client.post("/login", data={
        "email": "testingsample@test.com",
        "password": "123456",
    })

    response = test_client.get(url_for('whatever.url'), follow_redirects=True)
    assert response.status_code == 302
    # Check that the second request was to the index page.
    assert response.request.path == "/home"
