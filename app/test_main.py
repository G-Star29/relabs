import json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_msg_send_and_receive():
    with client.websocket_connect('/ws') as ws:
        message = {'message': 'Hello World'}
        ws.send_text(json.dumps(message))

        response = ws.receive_text()
        data = json.loads(response)

        assert data['message'] == 'Hello World'
        assert data['id'] == 1

        message = {'message': 'Hello World 2'}
        ws.send_text(json.dumps(message))

        response = ws.receive_text()
        data = json.loads(response)

        assert data['message'] == 'Hello World 2'
        assert data['id'] == 2

def test_restart_counter():
    with client.websocket_connect('/ws') as ws:
        message = {'message': 'Hello World'}
        ws.send_text(json.dumps(message))

        response = ws.receive_text()
        data = json.loads(response)

        assert data['message'] == 'Hello World'
        assert data['id'] == 1

    with client.websocket_connect('/ws') as ws:

        message = {'message': 'Hello World 2'}
        ws.send_text(json.dumps(message))

        response = ws.receive_text()
        data = json.loads(response)
        assert data['message'] == 'Hello World 2'
        assert data['id'] == 1
