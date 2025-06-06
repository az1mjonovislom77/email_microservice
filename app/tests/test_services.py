
import pytest
from app.services.email import EmailService
from app.db.session import SessionLocal
from datetime import datetime, timedelta


@pytest.fixture
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_send_email_service(db_session):
    service = EmailService(db_session)
    email = service.send_email(
        recipients=["test@example.com"],
        subject="Test",
        body="Test Body"
    )
    assert email is not None
    assert email.sender == "no-reply@example.com"

def test_get_stats(db_session):
    service = EmailService(db_session)
    stats = service.get_stats(
        date_from=datetime.now() - timedelta(days=1),
        date_to=datetime.now()
    )
    assert isinstance(stats.emails_sent, int)