import pytest
from unittest.mock import patch

@pytest.mark.usefixtures("client")
@patch("smtplib.SMTP")
def test_send_email(mock_smtp, client):
    # SMTP obyekti mock instance
    mock_smtp_instance = mock_smtp.return_value

    # POST so'rov yuborish /emails/send endpoint ga
    response = client.post(
        "/emails/send",
        json={
            "to": ["test@example.com"],
            "subject": "Test subject",
            "body": "Hello!"
        }
    )

    # Status kodi 200 bo'lishi kerak
    assert response.status_code == 200

    # SMTP server chaqirilganligini tekshirish
    mock_smtp.assert_called_once()

    # sendmail metodi chaqirilganligini tekshirish
    mock_smtp_instance.sendmail.assert_called_once()

@pytest.mark.usefixtures("client")
def test_get_emails(client):
    # GET so'rov yuborish /emails endpoint ga
    response = client.get("/emails")

    # Status kodi 200 bo'lishi kerak
    assert response.status_code == 200

@pytest.mark.usefixtures("client")
def test_get_email_stats(client):
    # GET so'rov yuborish /emails/stats endpoint ga query parametrlari bilan
    params = {
        "date_from": "2025-01-01T00:00:00",
        "date_to": "2025-12-31T23:59:59"
    }
    response = client.get("/emails/stats", params=params)

    # Status kodi 200 bo'lishi kerak
    assert response.status_code == 200
