import pytest
from server.app import create_app
from server.models import db as sqlalchemy_db
from server.config import TestingConfig

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    _app = create_app(TestingConfig)

    with _app.app_context():
        sqlalchemy_db.create_all()
        yield _app
        sqlalchemy_db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def db(app):
    """A fixture to provide the database instance."""
    return sqlalchemy_db
