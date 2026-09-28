from .conftest import csrf


def login(client, email):
    return client.post(
        "/auth/login",
        data={"csrf_token": csrf(client), "email": email, "password": "password123"},
    )


def test_public_pages_render(client):
    assert client.get("/").status_code == 200
    assert client.get("/catalog?q=Flask").status_code == 200
    assert client.get("/books/1").status_code == 200
    assert client.get("/auth/login").status_code == 200
    assert client.get("/auth/register").status_code == 200


def test_reader_pages_render(client):
    login(client, "reader@test.vn")
    assert client.get("/reader/dashboard").status_code == 200
    assert client.get("/reader/loans").status_code == 200
    assert client.get("/reader/profile").status_code == 200


def test_librarian_pages_render(client):
    login(client, "staff@test.vn")
    assert client.get("/librarian/dashboard").status_code == 200
    assert client.get("/librarian/books").status_code == 200
    assert client.get("/librarian/books/new").status_code == 200
    assert client.get("/librarian/loans").status_code == 200


def test_admin_pages_render(client):
    login(client, "admin@test.vn")
    assert client.get("/admin/dashboard").status_code == 200
    assert client.get("/admin/users").status_code == 200
    assert client.get("/admin/users/new").status_code == 200
    assert client.get("/admin/categories").status_code == 200
    assert client.get("/admin/categories/1/edit").status_code == 200
