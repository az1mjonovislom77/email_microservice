from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from app.api.schemas import (
    EmailSendRequest,
    EmailResponse,
    EmailStatsResponse,
    EmailListResponse
)
from app.services.email import EmailService
from app.db.session import get_db

router = APIRouter()

@router.post("/send", response_model=EmailResponse)
def send_email(
    email_data: EmailSendRequest,
    db: Session = Depends(get_db)
):
    try:
        return EmailService(db).send_email(
            recipients=email_data.to,
            subject=email_data.subject,
            body=email_data.body
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email sending failed: {str(e)}")

@router.get("/", response_model=List[EmailListResponse])
def list_emails(
    sender: Optional[str] = Query(None),
    recipient: Optional[str] = Query(None),
    subject: Optional[str] = Query(None),
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    try:
        return EmailService(db).get_emails(
            sender=sender,
            recipient=recipient,
            subject=subject,
            date_from=date_from,
            date_to=date_to
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve emails: {str(e)}")

@router.get("/stats", response_model=EmailStatsResponse)
def get_email_stats(
    date_from: datetime = Query(...),
    date_to: datetime = Query(...),
    db: Session = Depends(get_db)
):
    try:
        return EmailService(db).get_stats(date_from=date_from, date_to=date_to)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get statistics: {str(e)}")
