# Flask Users App

![Tests](https://github.com/fshakrun/FlaskUsersApp/actions/workflows/tests.yml/badge.svg)
![Coverage](https://img.shields.io/badge/coverage-98%25-brightgreen)
![Pytest](https://img.shields.io/badge/tests-pytest-orange)
![Allure](https://img.shields.io/badge/report-allure-purple)

Простое веб‑приложение на Flask для управления пользователями.
Для связи fshakrun@gmail.com

---

## 🚀 Функциональность

* Хранение пользователей в SQLite
* Получение списка пользователей
* Получение пользователя по ID
* Добавление нового пользователя
* Простой фронтенд на vanilla JS + Bootstrap
* API‑тесты на pytest
* Проверка JSON‑схемы ответа
* Параметризованные тесты
* Подсчёт test coverage
* Allure отчёты
* CI через GitHub Actions

---

## ▶️ Как запустить проект

### 1. Клонировать репозиторий

```bash
git clone <your-repo-url>
cd project
```

### 2. Создать виртуальное окружение (рекомендуется)

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

---

### 4. Запустить приложение

```bash
python app.py
```

Приложение будет доступно по адресу:

```
http://127.0.0.1:5000
```

---

## 🔌 API эндпоинты

### Получить всех пользователей

```
GET /users
```

### Получить пользователя по ID

```
GET /users/<id>
```

### Создать пользователя

```
POST /users
Content-Type: application/json
```

Пример тела запроса:

```json
{
  "name": "John Doe",
  "email": "john@example.com"
}
```

---

## 🧪 Тестирование

В проекте реализованы API‑тесты с использованием **pytest**.

### ✅ Что покрыто тестами

* позитивные сценарии API
* негативные сценарии
* валидация входных данных
* проверка JSON‑схемы ответа
* параметризованные тесты
* тестовая SQLite база в памяти

CI настроен на падение сборки при coverage < 90%.

---

### ▶️ Запуск тестов

```bash
pytest -v
```

### ▶️ Запуск с coverage

```bash
pytest --cov=. --cov-report=term-missing
```

**Текущее покрытие:** ~98%

---

## 📊 Allure отчёты

### 1. Запуск тестов с Allure

```bash
pytest --alluredir=allure-results
```

### 2. Открыть отчёт

```bash
allure serve allure-results
```

📌 Требуется установленный Allure CLI.

**Установка через npm:**

```bash
npm install -g allure-commandline
```

---

## ⚙️ CI

Проект использует **GitHub Actions** для автоматического запуска тестов при каждом push и pull request.

Pipeline выполняет:

* установку зависимостей
* запуск pytest
* подсчёт покрытия
* генерацию Allure results

---

## 🗄 База данных

Используется SQLite.

* при обычном запуске — файл БД
* в тестах — in‑memory база

---

## 🎯 Стек технологий

* Flask
* SQLite
* SQLAlchemy
* pytest
* Allure
* Bootstrap
* GitHub Actions

---
