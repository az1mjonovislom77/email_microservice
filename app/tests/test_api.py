from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

def get_date_range():
    end = datetime.utcnow()
    start = end - timedelta(days=1)
    return start.isoformat(), end.isoformat()

@patch("smtplib.SMTP")
def test_send_email(client, mock_smtp):
    mock_server = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_server

    response = client.post("/api/v1/emails/send", json={
        "to": ["test@example.com"],
        "subject": "Test Subject",
        "body": "Test Body"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["subject"] == "Test Subject"
    assert data["recipients"] == ["test@example.com"]

def test_list_emails(client):
    response = client.get("/api/v1/emails")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_filter_emails(client):
    response = client.get("/api/v1/emails?subject=Test")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_email_stats(client):
    date_from, date_to = get_date_range()
    response = client.get(f"/api/v1/emails/stats?date_from={date_from}&date_to={date_to}")
    assert response.status_code == 200
    data = response.json()
    assert "emails_sent" in data
    assert "emails_received" in data
