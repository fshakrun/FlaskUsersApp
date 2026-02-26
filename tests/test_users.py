import pytest
import allure
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


@allure.feature("Users API")
@allure.story("Get users list")
@allure.title("Получение пустого списка пользователей")
def test_get_users_empty(client):
    with allure.step("Отправляем GET /users"):
        response = client.get("/users")

    with allure.step("Проверяем статус и пустой список"):
        assert response.status_code == 200
        assert response.get_json() == []


@allure.feature("Users API")
@allure.story("Get users list")
@allure.title("Получение списка пользователей с данными")
def test_get_users_with_data(client, sample_user):
    with allure.step("Отправляем GET /users"):
        response = client.get("/users")
        data = response.get_json()

    with allure.step("Проверяем, что пользователь присутствует"):
        assert response.status_code == 200
        assert len(data) == 1
        assert data[0]["email"] == "test@example.com"


@allure.feature("Users API")
@allure.story("Get user by id")
@allure.title("Успешное получение пользователя по ID")
def test_get_user_by_id_success(client, sample_user):
    with allure.step("Запрашиваем пользователя по id"):
        response = client.get(f"/users/{sample_user}")
        data = response.get_json()

    with allure.step("Проверяем корректность ответа"):
        assert response.status_code == 200
        assert data["id"] == sample_user
        assert data["email"] == "test@example.com"


@allure.feature("Users API")
@allure.story("Get user by id")
@allure.title("Ошибка при запросе несуществующего пользователя")
def test_get_user_not_found(client):
    with allure.step("Запрашиваем несуществующий id"):
        response = client.get("/users/999")
        data = response.get_json()

    with allure.step("Проверяем 404 и текст ошибки"):
        assert response.status_code == 404
        assert data["error"] == "User not found"


@allure.feature("Users API")
@allure.story("Create user")
@allure.title("Успешное создание пользователя")
def test_create_user_success(client):
    payload = {"name": "John", "email": "john@example.com"}

    with allure.step("Отправляем POST /users с валидными данными"):
        response = client.post("/users", json=payload)
        data = response.get_json()

    with allure.step("Проверяем успешное создание"):
        assert response.status_code == 201
        assert data["email"] == payload["email"]


@allure.feature("Users API")
@allure.story("Create user validation")
@allure.title("Ошибка при отсутствии обязательных полей")
def test_create_user_missing_fields(client):
    with allure.step("Отправляем POST без email"):
        response = client.post("/users", json={"name": "Only Name"})
        data = response.get_json()

    with allure.step("Проверяем ошибку валидации"):
        assert response.status_code == 400
        assert "error" in data


@allure.feature("Users API")
@allure.story("Create user validation")
@allure.title("Ошибка при создании пользователя с дублирующим email")
def test_create_user_duplicate_email(client, sample_user):
    payload = {"name": "Another", "email": "test@example.com"}

    with allure.step("Пытаемся создать пользователя с существующим email"):
        response = client.post("/users", json=payload)
        data = response.get_json()

    with allure.step("Проверяем ошибку дубликата"):
        assert response.status_code == 400
        assert data["error"] == "Email already exists"


@allure.feature("Users API")
@allure.story("Create user validation")
@allure.title("Параметризованная проверка валидации пользователя")
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
    with allure.step(f"POST /users с payload={payload}"):
        response = client.post("/users", json=payload)

    with allure.step("Проверяем статус ответа"):
        assert response.status_code == expected_status


@allure.feature("Users API")
@allure.story("Response schema")
@allure.title("Проверка JSON-схемы пользователя")
def test_user_response_schema(client, sample_user):
    with allure.step("Получаем пользователя"):
        response = client.get(f"/users/{sample_user}")
        data = response.get_json()

    with allure.step("Валидируем JSON-схему"):
        validate(instance=data, schema=USER_SCHEMA)