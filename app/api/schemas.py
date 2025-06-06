from datetime import datetime
from typing import List
from pydantic import BaseModel, EmailStr

class EmailSendRequest(BaseModel):
    to: List[EmailStr]
    subject: str
    body: str

class EmailResponse(BaseModel):
    id: int
    sender: str
    recipients: List[str]
    subject: str
    body: str
    sent_at: datetime
    is_outgoing: bool

    class Config:
        orm_mode = True

class EmailListResponse(BaseModel):
    id: int
    sender: str
    recipients: List[str]
    subject: str
    sent_at: datetime

    class Config:
        orm_mode = True

class EmailStatsResponse(BaseModel):
    period_start: datetime
    period_end: datetime
    emails_sent: int
    emails_received: int