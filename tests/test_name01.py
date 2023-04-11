from crayfish_analysis_app.models import db
from crayfish_analysis_app.models import User
from flask import get_flashed_messages
from werkzeug.security import check_password_hash


def test_get_home(client):
    """
    GIVEN
    WHEN
    THEN
    """
    response = client.get("/home")
    assert response.status_code == 200


def test_post_signup_new_user(client):
    # Check if the region exists, it does then delete it
    exists = db.session.execute(
        db.select(User).filter_by(username="crayfish_king")
    ).scalar()
    if exists:
        db.session.execute(db.delete(User).where(User.username == "crayfish_king"))
        db.session.commit()

    response = client.post("/signup", data={
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
    assert check_password_hash(target.password, 'ilovecrayfish') == True


def test_post_signup_invalid_email(client):
    exists = db.session.execute(
        db.select(User).filter_by(username="Invalid_email")
    ).scalar()
    if exists:
        db.session.execute(db.delete(User).where(User.username == "Invalid_email"))
        db.session.commit()

    response = client.post("/signup", data={
        "username": "Invalid_email",
        "email": "I-am-invalid-email",
        "password1": "invalidemail",
        "password2": "invalidemail"
    })
    text = ''.join(get_flashed_messages())

    assert text == 'Email is invalid.'


def test_post_login(client, create_user):
    response = client.post("/login", data={
        "email": "testingsample@test.com",
        "password": "123456",
    })
    text = ''.join(get_flashed_messages())
    assert response.status_code == 302
    assert text == 'Logged in!'


def test_post_login_wrong_password(client, create_user):
    client.post("/login", data={
        "email": "testingsample@test.com",
        "password": "WrongPassword",
    })
    text = ''.join(get_flashed_messages())

    assert text == 'Password is incorrect.'


def test_post_login_wrong_email(client, create_user):
    client.post("/login", data={
        "email": "WrongEmail@test.com",
        "password": "123456",
    })
    text = ''.join(get_flashed_messages())

    assert text == 'Email does not exist.'


def test_post_delete_user(client, create_user):

    client.post("/login", data={
        "email": "testingsample@test.com",
        "password": "123456",
    })

    target = db.session.execute(
        db.select(User).filter_by(username="IamTest")
    ).scalar()

    target_id = target.id

    response = client.post(f"/delete-account/{target_id}")

    exist = db.session.execute(
        db.select(User).filter_by(username="IamTest")
    ).scalar()

    assert response.status_code == 302
    assert exist is None
