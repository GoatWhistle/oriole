from src.backend.main import app
from fastapi.testclient import TestClient
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address, enabled=False)
app.state.limiter = limiter

client = TestClient(app)


def test_health_check():
    response = client.get("/api/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}
