import pytest
from jsonschema import validate
from app import app as flask_app
from models import db, User

USER_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "email"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "email": {"type": "string"},
    },
}


def test_get_users_empty(client):
    response = client.get("/users")

    assert response.status_code == 200
    assert response.get_json() == []


def test_get_users_with_data(client, sample_user):
    response = client.get("/users")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["email"] == "test@example.com"


def test_get_user_by_id_success(client, sample_user):
    response = client.get(f"/users/{sample_user}")
    data = response.get_json()

    assert response.status_code == 200
    assert data["id"] == sample_user
    assert data["email"] == "test@example.com"


def test_get_user_not_found(client):
    response = client.get("/users/999")
    data = response.get_json()

    assert response.status_code == 404
    assert data["error"] == "User not found"


def test_create_user_success(client):
    payload = {"name": "John", "email": "john@example.com"}

    response = client.post("/users", json=payload)
    data = response.get_json()

    assert response.status_code == 201
    assert data["email"] == payload["email"]


def test_create_user_missing_fields(client):
    response = client.post("/users", json={"name": "Only Name"})
    data = response.get_json()

    assert response.status_code == 400
    assert "error" in data


def test_create_user_duplicate_email(client, sample_user):
    payload = {"name": "Another", "email": "test@example.com"}

    response = client.post("/users", json=payload)
    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "Email already exists"


@pytest.mark.parametrize(
    "payload, expected_status",
    [
        ({"name": "Alice", "email": "alice@test.com"}, 201),
        ({"name": "", "email": "bad@test.com"}, 400),
        ({"name": "NoEmail"}, 400),
        ({}, 400),
    ],
)
def test_create_user_validation(client, payload, expected_status):
    response = client.post("/users", json=payload)
    assert response.status_code == expected_status

def test_user_response_schema(client, sample_user):
    response = client.get(f"/users/{sample_user}")
    data = response.get_json()

    validate(instance=data, schema=USER_SCHEMA)