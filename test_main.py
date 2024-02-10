import io
import pytest
from fastapi.testclient import TestClient
from main import app



@pytest.fixture
def client():
    return TestClient(app)



def test_upload_file_and_create_route(client):

    # Создаем тестовые данные для CSV файла

    with open("test.csv", "r") as file:
        csv_data = file.read()

    # Отправляем POST запрос на эндпоинт с тестовыми данными

    response = client.post("/api/routes/", files={"file": ("test.csv", io.BytesIO(csv_data.encode()), "text/csv")})

    # Проверяем, что запрос завершился успешно

    assert response.status_code == 200

    # Проверяем, что возвращаемый результат содержит ожидаемый формат данных

    assert "id" in response.json()
    assert "points" in response.json()



def test_upload_invalid_file_type(client):

    # Отправляем POST запрос с файлом, не в формате CSV

    response = client.post("/api/routes/", files={"file": ("test.txt", io.BytesIO(b"some text"), "text/plain")})

    # Проверяем, что сервер возвращает ожидаемый статус код ошибки

    assert response.status_code == 400

    # Проверяем, что сообщение об ошибке соответствует ожидаемому

    assert response.json()["detail"] == "Файл должен быть в формате CSV."