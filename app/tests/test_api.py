import pytest
from unittest.mock import patch

@pytest.mark.usefixtures("client")
@patch("smtplib.SMTP")
def test_send_email(mock_smtp, client):
    mock_smtp_instance = mock_smtp.return_value

    response = client.post(
        "/api/v1/emails/send",
        json={
            "to": ["test@example.com"],
            "subject": "Test subject",
            "body": "Hello!"
        }
    )

    assert response.status_code == 200

@pytest.mark.usefixtures("client")
def test_get_emails(client):
    response = client.get("/api/v1/emails")
    assert response.status_code == 200

@pytest.mark.usefixtures("client")
def test_get_email_stats(client):
    params = {
        "date_from": "2025-01-01T00:00:00",
        "date_to": "2025-12-31T23:59:59"
    }
    response = client.get("/api/v1/emails/stats", params=params)
    assert response.status_code == 200
