from crayfish_analysis_app.models import db
from crayfish_analysis_app.models import User
from pathlib import Path
import sqlite3


def test_get_home(client):
    """
    GIVEN a running Flask app
    WHEN an HTTP GET request is made to '/noc'
    THEN the status code should be 200, the code 'AFG' should be in the response data and the content type "application/json"
    """
    response = client.get("/home")
    assert response.status_code == 200


def test_post_signup_new_user(client):
    # Check if the region exists, it does then delete it
    exists = db.session.execute(
        db.select(User).filter_by(username="ucl_benny")
    ).scalar()
    if exists:
        db.session.execute(db.delete(User).where(User.username == "ucl_benny"))
        db.session.commit()

    response = client.post("/signup", data={
        "username": "ucl_benny",
        "email": "bennyuclsample@gmail.com",
        "password1": "123456",
        "password2": "123456"
    })

    target = db.session.execute(
        db.select(User).filter_by(username="ucl_benny")
    ).scalar()

    assert response.status_code == 302
    assert target.email == "bennyuclsample@gmail.com"


def test_post_delete_user(client):
    # Check if the region exists, it does then delete it
    exists = db.session.execute(
        db.select(User).filter_by(username="ucl_benny")
    ).scalar()
    if exists:
        db.session.execute(db.delete(User).where(User.username == "ucl_benny"))
        db.session.commit()

    target = db.session.execute(
        db.select(User).filter_by(username="abc")
    ).scalar()

    assert target is None
