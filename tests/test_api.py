from main import app, classifier
from unittest.mock import MagicMock
from fastapi.testclient import TestClient

client = TestClient(app)

# Проверка работоспособности API путем отправки зароса к корневому маршруту эндпоинта
def test_unit_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the FastAPI app! Use the /check_prompt endpoint."
    }
