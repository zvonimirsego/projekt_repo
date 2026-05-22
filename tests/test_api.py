from fastapi.testclient import TestClient
from server.main import app
from database.py_classes import Users

client = TestClient(app)


def test_create_user():

    response = client.post(
        "/users/",
        json={
            "email": "test@gmail.com",
            "first_name": "Ken",
            "last_name": "Levine",
            "password": "1234",
        },
    )

    assert response.status_code == 200


def test_delete_user():

    response = client.delete("/users/test@gmail.com")

    assert response.status_code == 200


def test_update_password():

    user = Users("test@gmail.com", "Ken", "Levine", "1234")

    user.add()

    response = client.put("/users/test@gmail.com", json={"password": "newpass"})

    assert response.status_code == 200


def test_get_user_api():

    user = Users("api@gmail.com", "Ken", "Levine", "1234")

    user.add()

    response = client.get("/users/api@gmail.com")

    assert response.status_code == 200
