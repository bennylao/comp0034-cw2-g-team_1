import pytest
import config
from crayfish_analysis_app import create_app
from crayfish_analysis_app.models import db, User
from werkzeug.security import generate_password_hash


@pytest.fixture(scope="session")
def app():
    """Create a Flask app configured for testing"""
    app = create_app(config.TestingConfig)
    yield app


@pytest.fixture(scope="function")
def client(app):
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
