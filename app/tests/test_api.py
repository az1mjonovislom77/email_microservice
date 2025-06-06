from unittest.mock import patch
import pytest

def test_example():
    assert True  # Oddiy test misol uchun

@patch("smtplib.SMTP")
def test_send_email(mock_smtp, client):
    # SMTP serverni mock qilish
    mock_smtp_instance = mock_smtp.return_value

    # Sizning email yuborish logikangizni shu yerda chaqiring
    response = client.post(
        "/send-email",
        json={
            "sender": "no-reply@example.com",
            "recipients": ["test@example.com"],
            "subject": "Test subject",
            "body": "Hello!"
        }
    )
    assert response.status_code == 200
    # Qo‘shimcha assertlar kiritishingiz mumkin
    mock_smtp.assert_called_once()
    mock_smtp_instance.sendmail.assert_called_once()

# Boshqa testlar shu faylda davom ettirilishi mumkin
