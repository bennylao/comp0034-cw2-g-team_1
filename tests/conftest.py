import pytest
import config
from crayfish_analysis_app import create_app
from crayfish_analysis_app.models import db, User
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


# Used for Selenium tests
@pytest.fixture(scope="session")
def chrome_driver():
    """Selenium webdriver with options to support running in GitHub actions
    Note:
        For CI: `headless` not commented out
        For running on your computer: `headless` to be commented out
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    driver = Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


