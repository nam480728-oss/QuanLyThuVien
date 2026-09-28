from sqlalchemy import select

from app.extensions import db
from app.models import User
from .conftest import csrf


def test_register_creates_reader(client, app):
    response = client.post(
        "/auth/register",
        data={
            "csrf_token": csrf(client),
            "full_name": "Bạn Đọc Mới",
            "email": "new@test.vn",
            "password": "password123",
            "confirm_password": "password123",
        },
    )
    assert response.status_code == 302
    with app.app_context():
        user = db.session.scalar(select(User).where(User.email == "new@test.vn"))
        assert user is not None
        assert user.role == "reader"
        assert user.check_password("password123")


def test_login_and_role_protection(client):
    response = client.post(
        "/auth/login",
        data={"csrf_token": csrf(client), "email": "reader@test.vn", "password": "password123"},
    )
    assert response.status_code == 302
    assert client.get("/reader/dashboard").status_code == 200
    assert client.get("/admin/dashboard").status_code == 403
