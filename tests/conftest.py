import sys
import os
import pytest
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import app as flask_app
from models import db, User


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    flask_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    with flask_app.app_context():
        db.drop_all()
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def sample_user(app):
    with app.app_context():
        user = User(name="Test User", email="test@example.com")
        db.session.add(user)
        db.session.commit()
        return user.id

