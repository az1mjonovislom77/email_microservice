from app.db.session import Base  
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ARRAY

class Email(Base):
    __tablename__ = "emails"
    
    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String(255), nullable=False)
    recipients = Column(ARRAY(String), nullable=False)
    subject = Column(String(255))
    body = Column(Text)
    sent_at = Column(DateTime, nullable=False)
    is_outgoing = Column(Boolean, nullable=False)