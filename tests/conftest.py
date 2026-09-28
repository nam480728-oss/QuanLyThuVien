import pytest

from app import create_app
from app.extensions import db
from app.models import Author, Book, Category, User
from config import TestConfig


@pytest.fixture()
def app():
    application = create_app(TestConfig)
    with application.app_context():
        db.create_all()
        category = Category(name="Công nghệ")
        author = Author(name="Tác giả Test")
        book = Book(
            isbn="TEST-001",
            title="Flask thực chiến",
            category=category,
            authors=[author],
            total_copies=2,
            available_copies=2,
        )
        reader = User(full_name="Độc giả Test", email="reader@test.vn", role="reader")
        reader.set_password("password123")
        staff = User(full_name="Thủ thư Test", email="staff@test.vn", role="librarian")
        staff.set_password("password123")
        admin = User(full_name="Quản trị Test", email="admin@test.vn", role="admin")
        admin.set_password("password123")
        db.session.add_all([book, reader, staff, admin])
        db.session.commit()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def csrf(client):
    with client.session_transaction() as session:
        session["csrf_token"] = "test-token"
    return "test-token"
