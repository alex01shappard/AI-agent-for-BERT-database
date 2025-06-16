from api import app
from unittest.mock import patch
from fastapi.testclient import TestClient

client = TestClient(app)

# Проверка работоспособности API путем отправки зароса к корневому маршруту
# эндпоинта


def test_unit_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the FastAPI app!"
                   "Use the /check_prompt endpoint."
    }

# Проверка работоспособности API путем отправки запроса по маршруту
# /check_prompt. Языковая модель заменяется на заглушку в целях тестирования


@patch("agent.BertFilter")
@patch("agent.main_with_prompt")
def test_check_prompt_valid(mock_main_with_prompt, MockBertFilter):
    mock_bert_instance = MockBertFilter.return_value
    mock_bert_instance.classify_prompt.return_value = 0
    mock_main_with_prompt.return_value = "Mocked Llama response"

    response = client.post("/check_prompt", json={"prompt": "Hello"})
    assert response.status_code == 200
    assert response.json() == {"answer": "Mocked Llama response"}

# Провека корректной обработки пустого запроса


def test_check_prompt_missing_field():
    response = client.post("/check_prompt", json={})
    assert response.status_code == 422
