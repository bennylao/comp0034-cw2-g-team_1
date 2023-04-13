from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from crayfish_analysis_app.models import db
from crayfish_analysis_app.models import User, Post, Like, Comment, Crayfish1, Crayfish2
from werkzeug.security import check_password_hash, generate_password_hash
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
    WHEN the About page is accessed
    THEN the page title should be "About"
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
    WHEN the dashboard is accessed
    THEN the url should change to the dashboard url
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
    WHEN the dashboard is accessed
    THEN the value of the page title should be "Crayfish Analysis Dashboard"
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

    # delete the user if it exists
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


def test_login(chrome_driver, run_app_win, flask_port, test_client, create_user):
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
    email.send_keys('testingsample@test.com')

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


def test_forum_post(chrome_driver, run_app_win, flask_port, test_client, create_user):
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
    email.send_keys('testingsample@test.com')

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


def test_like(chrome_driver, run_app_win, flask_port, test_client, create_user):
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
    email.send_keys('testingsample@test.com')

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


def test_comment(chrome_driver, run_app_win, flask_port, test_client, create_user):
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
    email.send_keys('testingsample@test.com')

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


def test_crayfish1_page_title(chrome_driver, run_app_win, flask_port):
    """
    GIVEN a running app
    WHEN the crayfish1 page is accessed
    THEN the page title should be "Crayfish Caught Using Different Trapping Methods"
    """
    url = f"http://localhost:{flask_port}/crayfish1"
    chrome_driver.get(url)
    title = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'h1'))
    )
    assert title.text == "Crayfish Caught Using Different Trapping Methods"


def test_crayfish2_page_title(chrome_driver, run_app_win, flask_port):
    """
    GIVEN a running app
    WHEN the crayfish2 page is accessed
    THEN the page title should be "Crayfish Weights and Lengths"
    """
    url = f"http://localhost:{flask_port}/crayfish2"
    chrome_driver.get(url)
    title = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'h1'))
    )
    assert title.text == "Crayfish Lengths and Weights"


def test_reset_password_by_email(chrome_driver, run_app_win, flask_port, test_client,
                                 create_user_for_resetting_password):
    """
    GIVEN a running app
    WHEN changing password using forgot password method
    THEN the password is changed in the database
    """
    url = f"http://localhost:{flask_port}/login"
    chrome_driver.get(url)

    forgot_pwd = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/form/div/div/a'))
    )
    forgot_pwd.click()
    input_email = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, 'email')))
    input_email.send_keys("sample_reset_pwd@test.com")
    btn = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/form/div/div/button'))
    )
    btn.click()

    user = db.session.execute(
        db.select(User).filter_by(email="sample_reset_pwd@test.com")
    ).scalar()

    url = (f"http://localhost:{flask_port}/" + "reset-password/" + str(user.get_reset_token()))

    chrome_driver.get(url)

    password1 = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, 'reset_password1'))
    )
    password1.send_keys("aaaaaa")

    password2 = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, 'reset_password2'))
    )
    password2.send_keys("aaaaaa")

    change = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div/form/div/div/button'))
    )

    change.click()

    assert check_password_hash(user.password, 'aaaaaa') is True

def test_change_password(chrome_driver, run_app_win, flask_port, test_client, create_user_for_resetting_password):
    """
    GIVEN a running app
    WHEN logging in
    AND changing the password 
    THEN the password the password in the database should be
        changed to the new password
    """
    url = f"http://localhost:{flask_port}/login"
    chrome_driver.get(url)

    user = db.session.execute(
        db.select(User).filter_by(email="sample_reset_pwd@test.com")
    ).scalar()

    user.password = generate_password_hash("123456", method='sha256')
    db.session.commit()

    input_email = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, 'email')))
    input_email.send_keys("sample_reset_pwd@test.com")

    input_password = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, 'password')))
    input_password.send_keys("123456")

    login_button = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div/form/div/div/button"))
    )
    
    login_button.click()

    chrome_driver.get(f"http://localhost:{flask_port}/account-management")

    old_password = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, 'old_password')))
    
    old_password.send_keys("123456")

    new_password1 = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, 'new_password1')))
    
    new_password1.send_keys("1234567")

    new_password2 = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, 'new_password2')))
    
    new_password2.send_keys("1234567")

    change_pass = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/div[1]/div/div/form/div/div/button"))
    )

    change_pass.click()
    
    assert check_password_hash(user.password, '1234567') is True 


    

def test_database_1_add_record(chrome_driver, run_app_win, flask_port, test_client, create_user):
    url = f"http://localhost:{flask_port}/login"
    chrome_driver.get(url)

    email = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, 'email'))
    )
    email.send_keys('testingsample@test.com')

    password = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, 'password'))
    )
    password.send_keys('123456')

    login_button = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div/form/div/div/button'))
    )
    login_button.click()

    database_1 = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="navbar"]/div/a[5]'))
    )
    database_1.click()

    add_record = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/form/button[2]'))
    )
    add_record.click()

    site = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, 'site'))
    )
    site.send_keys('Testing_Site')

    method = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, 'method'))
    )
    method.send_keys('Testing_Method')

    gender = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, 'gender'))
    )
    gender.send_keys('Testing_Gender')

    length = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, 'length'))
    )
    length.send_keys('1000000')

    submit = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[1]/form/div/div/button'))
    )
    submit.click()
    chrome_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    target = db.session.execute(
        db.select(Crayfish1).filter_by(site="Testing_Site")
    ).scalar()

    assert target.method == 'Testing_Method'

    db.session.execute(db.delete(Crayfish1).where(Crayfish1.site == "Testing_Site"))
    db.session.commit()


def test_database_1_delete_record(chrome_driver, run_app_win, flask_port, test_client, create_user,
                                  create_record_crayfish1):
    url = f"http://localhost:{flask_port}/login"
    chrome_driver.get(url)

    email = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, 'email'))
    )
    email.send_keys('testingsample@test.com')

    password = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, 'password'))
    )
    password.send_keys('123456')

    login_button = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div/form/div/div/button'))
    )
    login_button.click()

    database_1 = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="navbar"]/div/a[5]'))
    )
    database_1.click()

    chrome_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    target = db.session.execute(
        db.select(Crayfish1).filter_by(site="Test_site")
    ).scalar()

    # Ensure the driver has scrolled to the bottom and the delete button is visible and clickable
    time.sleep(5)

    delete = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f'/html/body/div/div/div/div/div/ul/li[{target.id}]/div[2]/form/button'))
    )
    delete.click()



def test_database_1_delete_record(chrome_driver, run_app_win, flask_port, test_client, create_user,
                                  create_record_crayfish1):
    url = f"http://localhost:{flask_port}/login"
    chrome_driver.get(url)

    email = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, 'email'))
    )
    email.send_keys('testingsample@test.com')

    password = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.ID, 'password'))
    )
    password.send_keys('123456')

    login_button = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div/form/div/div/button'))
    )
    login_button.click()

    database_1 = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="navbar"]/div/a[5]'))
    )
    database_1.click()

    chrome_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    target = db.session.execute(
        db.select(Crayfish1).filter_by(site="Test_site")
    ).scalar()

    # Ensure the driver has scrolled to the bottom and the delete button is visible and clickable
    time.sleep(5)

    delete = WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f'/html/body/div/div/div/div/div/ul/li[{target.id}]/div[2]/form/button'))
    )
    delete.click()

    target_after = db.session.execute(
        db.select(Crayfish1).filter_by(site="Test_site")
    ).scalar()

    assert target_after is None
