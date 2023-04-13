from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from crayfish_analysis_app.models import db
from crayfish_analysis_app.models import User, Post, Like, Comment
from werkzeug.security import check_password_hash
from flask import get_flashed_messages
import time


def test_home_page_title(chrome_driver, run_app_win, flask_port):
    """
    GIVEN a running app
    WHEN the homepage is accessed
    THEN the value of the page title should be "Home"
    """
    url = f"http://localhost:{flask_port}/"
    chrome_driver.get(url)
    chrome_driver.implicitly_wait(3)
    assert chrome_driver.title == "Home"


def test_homepage_subheadings(chrome_driver, run_app_win, flask_port):
    """
    GIVEN a running app
    WHEN the homepage is accessed
    THEN the value of the page subheadings should be "Protect Ecosystems"
    "Monitor Populations" and "Data Dashboard"
    """
    url = f"http://localhost:{flask_port}"
    chrome_driver.get(url)
    heading1 = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div/div/div/div/div[3]/div/h5'))
    )
    heading2 = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div/div/div/div/div[2]/div/h5'))
    )
    heading3 = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div/div/div/div/div[1]/div/h5'))
    )
    assert heading1.text == "Data Dashboard"
    assert heading2.text == "Monitor Populations"
    assert heading3.text == "Protect Ecosystems"


def test_forum_page_title(chrome_driver, run_app_win, flask_port):
    """
    GIVEN a running app
    WHEN the form page is accessed
    THEN the page title should be "Forum Posts"
    """
    url = f"http://localhost:{flask_port}/forum"
    chrome_driver.get(url)
    title = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/h1'))
    )
    assert title.text == "Forum Posts"


def test_about_page_title(chrome_driver, run_app_win, flask_port):
    """
    GIVEN a running app
    WHEN the form page is accessed
    THEN the page title should be "Forum Posts"
    """
    url = f"http://localhost:{flask_port}/about"
    chrome_driver.get(url)
    title = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/h1'))
    )
    assert title.text == "About Us"


def test_link_to_dashboard(chrome_driver, run_app_win, flask_port):
    """
    GIVEN a running app
    WHEN the homepage is accessed
    THEN the value of the page title should be "Home"
    """
    url = f"http://localhost:{flask_port}/"
    chrome_driver.get(url)
    link_to_dashboard = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="navbar"]/div/a[2]'))
    )
    link_to_dashboard.click()
    current_url = chrome_driver.current_url
    assert current_url == f"http://localhost:{flask_port}/dashboard/"


def test_dashboard_title(chrome_driver, run_app_win, flask_port):
    """
    GIVEN a running app
    WHEN the homepage is accessed
    THEN the value of the page title should be "Home"
    """
    url = f"http://localhost:{flask_port}/dashboard/"
    chrome_driver.get(url)
    heading = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="react-entry-point"]/div/div[1]/div/div/div/h1'))
    )
    assert heading.text == "Crayfish Analysis Dashboard"


def test_signup(chrome_driver, run_app_win, flask_port, test_client):
    """
    GIVEN a running app
    WHEN signing up is successful
    THEN the sign-up information should be in database
    """

    url = f"http://localhost:{flask_port}/signup"
    chrome_driver.get(url)

    exists = db.session.execute(
        db.select(User).filter_by(username="iamusername")
    ).scalar()
    if exists:
        db.session.execute(db.delete(User).where(User.username == "iamusername"))
        db.session.commit()

    email = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, 'email'))
    )
    email.send_keys('iamemail@gmail.com')
    username = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, 'username'))
    )
    username.send_keys('iamusername')
    password1 = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, 'password1'))
    )
    password1.send_keys('123456')
    password2 = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, 'password2'))
    )
    password2.send_keys('123456')
    signup_button = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div/form/div/div/button'))
    )
    signup_button.click()

    target = db.session.execute(
        db.select(User).filter_by(username="iamusername")
    ).scalar()

    assert target.email == "iamemail@gmail.com"
    assert check_password_hash(target.password, '123456') is True


def test_login(chrome_driver, run_app_win, flask_port, test_client):
    """
    GIVEN a running app
    WHEN loging in is successful
    THEN the url should be the home page
    """
    url = f"http://localhost:{flask_port}/login"
    chrome_driver.get(url)

    email = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, 'email'))
    )
    email.send_keys('iamemail@gmail.com')

    password = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, 'password'))
    )
    password.send_keys('123456')

    login_button = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div/form/div/div/button'))
    )
    login_button.click()

    current_url = chrome_driver.current_url
    assert current_url == f"http://localhost:{flask_port}/home"


def test_forum_post(chrome_driver, run_app_win, flask_port, test_client):
    """
    GIVEN a running app
    WHEN loging in is successful
    AND going to the forum page and making a new post
    THEN the message in the post should be in the forum page
    """
    url = f"http://localhost:{flask_port}/login"
    chrome_driver.get(url)

    db.session.execute(db.delete(Post))
    db.session.commit()

    email = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, 'email'))
    )
    email.send_keys('iamemail@gmail.com')

    password = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, 'password'))
    )
    password.send_keys('123456')

    login_button = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div/form/div/div/button'))
    )
    login_button.click()

    forum = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="navbar"]/div/a[3]'))
    )
    forum.click()

    create_post = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/a/button'))
    )
    create_post.click()

    text_post = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, 'text'))
    )

    text_post.send_keys('This is a new post that I made.')

    submit = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div/div/form/div/button'))
    )
    submit.click()

    current_url = chrome_driver.page_source

    search_text = 'This is a new post that I made.'

    assert search_text in current_url


def test_like(chrome_driver, run_app_win, flask_port, test_client):
    """
    GIVEN a running app
    WHEN loging in is successful
    AND going to the forum page and making a new post
    AND pressing the like button
    THEN the like number should be one
    """
    url = f"http://localhost:{flask_port}/login"
    chrome_driver.get(url)

    db.session.execute(db.delete(Post))
    db.session.execute(db.delete(Like))
    db.session.commit()

    email = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, 'email'))
    )
    email.send_keys('iamemail@gmail.com')

    password = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, 'password'))
    )
    password.send_keys('123456')

    login_button = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div/form/div/div/button'))
    )
    login_button.click()

    forum = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="navbar"]/div/a[3]'))
    )
    forum.click()

    create_post = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/a/button'))
    )
    create_post.click()

    text_post = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, 'text'))
    )

    text_post.send_keys('This is a new post that I made.')

    submit = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div/div/form/div/button'))
    )
    submit.click()

    like = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="posts"]/div[1]/div[1]/div/a'))
    )

    like.click()

    assert WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="posts"]/div/div[1]/div'))
    ).text == "1"


def test_comment(chrome_driver, run_app_win, flask_port, test_client):
    """
    GIVEN a running app
    WHEN loging in is successful
    AND going to the forum page and making a new post
    AND pressing the like button
    THEN the like number should be one
    """
    url = f"http://localhost:{flask_port}/login"
    chrome_driver.get(url)

    db.session.execute(db.delete(Post))
    db.session.execute(db.delete(Like))
    db.session.execute(db.delete(Comment))
    db.session.commit()

    email = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, 'email'))
    )
    email.send_keys('iamemail@gmail.com')

    password = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, 'password'))
    )
    password.send_keys('123456')

    login_button = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div/form/div/div/button'))
    )
    login_button.click()

    forum = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="navbar"]/div/a[3]'))
    )
    forum.click()

    create_post = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/a/button'))
    )
    create_post.click()

    text_post = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, 'text'))
    )

    text_post.send_keys('This is a new post that I made.')

    submit = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div/div/form/div/button'))
    )
    submit.click()

    comment = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div/div/div/div/div[2]/form/input'))
    )
    comment.send_keys('This is a new comment that I made.')

    comment_button = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="posts"]/div/div[2]/form/button'))
    )
    comment_button.click()

    view_comment = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="posts"]/div/div[2]/p/a/small'))
    )
    view_comment.click()
    source = chrome_driver.page_source

    assert 'This is a new comment that I made.' in source
