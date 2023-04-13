import pytest
import config
from crayfish_analysis_app import create_app
from crayfish_analysis_app.models import db, User, Crayfish1
from werkzeug.security import generate_password_hash
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
import subprocess
import socket


@pytest.fixture(scope="session")
def app():
    """Create a Flask app configured for testing"""
    app = create_app(config.TestingConfig)
    yield app


@pytest.fixture(scope="function")
def test_client(app):
    """ Flask test client within an application context. """
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            yield testing_client


@pytest.fixture(scope="function")
def create_user():
    # Check if the region exists, it does then delete it
    exists = db.session.execute(
        db.select(User).filter_by(username="IamTest")
    ).scalar()
    if not exists:
        new_user = User(email='testingsample@test.com', username='IamTest',
                        password=generate_password_hash('123456', method='sha256'))
        db.session.add(new_user)
        db.session.commit()


@pytest.fixture(scope="function")
def create_user_for_resetting_password():
    # Check if the region exists, it does then delete it
    exists = db.session.execute(
        db.select(User).filter_by(username="User_for_reset_pwd")
    ).scalar()
    if not exists:
        new_user = User(email='sample_reset_pwd@test.com', username='User_for_reset_pwd',
                        password=generate_password_hash('123456', method='sha256'))
        db.session.add(new_user)
        db.session.commit()


@pytest.fixture(scope="function")
def create_record_crayfish1():
    # Check if the region exists, it does then delete it
    exists = db.session.execute(
        db.select(Crayfish1).filter_by(site="Test_site")
    ).scalar()
    if not exists:
        new_user = Crayfish1(site='Test_site', method='Test_method',
                             gender='M', length='100000000000')
        db.session.add(new_user)
        db.session.commit()


# Used for Selenium tests
@pytest.fixture(scope="class")
def chrome_driver():
    """Selenium webdriver with options to support running in GitHub actions
    Note:
        For CI: headless not commented out
        For running on your computer: headless to be commented out
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    driver = Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture(scope="module")
def flask_port():
    """Ask OS for a free port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        addr = s.getsockname()
        port = addr[1]
        return port


@pytest.fixture(scope="module")
def run_app_win(flask_port):
    """Runs the Flask app for live server testing on Windows"""
    server = subprocess.Popen(
        [
            "flask",
            "--app",
            "crayfish_analysis_app:create_app('config.TestingConfig')",
            "run",
            "--port",
            str(flask_port),
        ]
    )
    try:
        yield server
    finally:
        server.terminate()
