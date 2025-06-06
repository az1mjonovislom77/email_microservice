import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session
from app.db.models import Email
from app.api.schemas import EmailResponse, EmailStatsResponse, EmailListResponse
from app.core.config import settings
from app.core.logger import logger

class EmailService:
    def __init__(self, db_session: Session):
        self.db = db_session

    def send_email(self, recipients: List[str], subject: str, body: str) -> EmailResponse:
        try:
            msg = MIMEMultipart()
            msg['From'] = settings.SMTP_USER
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'html' if '<html>' in body.lower() else 'plain'))
            
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                if settings.SMTP_PORT != 1025:  
                    server.starttls()
                    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)

            email_record = Email(
                sender=settings.SMTP_USER,
                recipients=recipients,
                subject=subject,
                body=body,
                sent_at=datetime.utcnow(),
                is_outgoing=True
            )
            self.db.add(email_record)
            self.db.commit()
            self.db.refresh(email_record)
            
            return EmailResponse.from_orm(email_record)
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to send email: {str(e)}")
            raise

    def get_emails(self,
                 sender: Optional[str] = None,
                 recipient: Optional[str] = None,
                 subject: Optional[str] = None,
                 date_from: Optional[datetime] = None,
                 date_to: Optional[datetime] = None) -> List[EmailListResponse]:
        
        query = self.db.query(Email)
        
        if sender:
            query = query.filter(Email.sender == sender)
        if recipient:
            query = query.filter(Email.recipients.contains([recipient]))
        if subject:
            query = query.filter(Email.subject.contains(subject))
        if date_from:
            query = query.filter(Email.sent_at >= date_from)
        if date_to:
            query = query.filter(Email.sent_at <= date_to)
        
        emails = query.order_by(Email.sent_at.desc()).all()
        return [EmailListResponse.from_orm(email) for email in emails]

    def get_stats(self,
                date_from: datetime,
                date_to: datetime) -> EmailStatsResponse:
        
        sent = self.db.query(Email).filter(
            Email.is_outgoing == True,
            Email.sent_at >= date_from,
            Email.sent_at <= date_to
        ).count()
        
        received = self.db.query(Email).filter(
            Email.is_outgoing == False,
            Email.sent_at >= date_from,
            Email.sent_at <= date_to
        ).count()
        
        return EmailStatsResponse(
            period_start=date_from,
            period_end=date_to,
            emails_sent=sent,
            emails_received=received
        )