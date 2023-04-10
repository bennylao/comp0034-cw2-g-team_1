import pytest
import config
from crayfish_analysis_app import create_app


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
