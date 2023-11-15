import json
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch


mock_chat_data = [
    json.dumps({"nickname": "tester", "text": "Hello", "instruction": "", "date": "2021-01-01T00:00:00"}),
    json.dumps({"nickname": "tester2", "text": "Hi there!", "instruction": "", "date": "2021-01-02T00:00:00"})
]


@patch("os.environ", {"API_KEY": "test"})
def test_post_message(client: TestClient, mocker: MagicMock):
    mock_lpush = mocker.patch('app.chat.redis_client.lpush')
    mock_ltrim = mocker.patch('app.chat.redis_client.ltrim')
    mock_lrange = mocker.patch('app.chat.redis_client.lrange', return_value=mock_chat_data)
    mocker.patch('app.chat.redis_client.delete')

    response = client.post("/v1/chats/test_chat/messages", json={"nickname": "tester", "text": "Hello"}, headers={"X-API-KEY": "test"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert "tester" in [msg["nickname"] for msg in data]
    mock_lpush.assert_called()
    mock_ltrim.assert_called()
    mock_lrange.assert_called_with("test_chat", 0, 49)


@patch("os.environ", {"API_KEY": "test"})
def test_get_messages(client: TestClient, mocker: MagicMock):
    mocker.patch('app.chat.redis_client.lpush')
    mocker.patch('app.chat.redis_client.ltrim')
    mock_lrange = mocker.patch('app.chat.redis_client.lrange', return_value=mock_chat_data)
    mocker.patch('app.chat.redis_client.delete')

    response = client.get("/v1/chats/test_chat/messages", headers={"X-API-KEY": "test"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    mock_lrange.assert_called_with("test_chat", 0, 49)


@patch("os.environ", {"API_KEY": "test"})
def test_clear_messages(client: TestClient, mocker: MagicMock):
    mocker.patch('app.chat.redis_client.lpush')
    mocker.patch('app.chat.redis_client.ltrim')
    mock_lrange = mocker.patch('app.chat.redis_client.lrange', return_value=[])
    mock_delete = mocker.patch('app.chat.redis_client.delete')

    response = client.patch("/v1/chats/test_chat/clear", headers={"X-API-KEY": "test"})
    assert response.status_code == 200
    data = response.json()
    assert data == []
    mock_delete.assert_called_with("test_chat")

    response = client.get("/v1/chats/test_chat/messages", headers={"X-API-KEY": "test"})
    assert response.json() == []
    mock_lrange.assert_called_with("test_chat", 0, 49)
