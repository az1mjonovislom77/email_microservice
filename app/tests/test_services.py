from unittest.mock import patch, MagicMock
from app.services.email import EmailService
from datetime import datetime, timedelta

@patch("smtplib.SMTP")
def test_send_email_service(mock_smtp, db_session):
    mock_server = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_server

    service = EmailService(db_session)
    result = service.send_email(
        recipients=["test@example.com"],
        subject="Test subject",
        body="Hello!"
    )

    assert result.subject == "Test subject"
    assert result.recipients == ["test@example.com"]
    assert result.is_outgoing is True

def test_get_stats(db_session):
    service = EmailService(db_session)
    result = service.get_stats(
        date_from=datetime.utcnow() - timedelta(days=1),
        date_to=datetime.utcnow()
    )

    assert isinstance(result.emails_sent, int)
    assert isinstance(result.emails_received, int)
