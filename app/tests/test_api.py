import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from app.main import app

client = TestClient(app)

def test_send_email():
    response = client.post(
        "/api/v1/emails/send",
        json={
            "to": ["test@example.com"],
            "subject": "Test Subject",
            "body": "Test Body"
        }
    )
    assert response.status_code == 200
    assert "id" in response.json()

def test_list_emails():
    response = client.get("/api/v1/emails")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_filter_emails():
    date_from = (datetime.now() - timedelta(days=1)).isoformat()
    date_to = datetime.now().isoformat()
    response = client.get(
        f"/api/v1/emails?date_from={date_from}&date_to={date_to}"
    )
    assert response.status_code == 200

def test_email_stats():
    date_from = (datetime.now() - timedelta(days=7)).isoformat()
    date_to = datetime.now().isoformat()
    response = client.get(
        f"/api/v1/emails/stats?date_from={date_from}&date_to={date_to}"
    )
    assert response.status_code == 200
    assert "emails_sent" in response.json()