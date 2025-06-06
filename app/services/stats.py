from datetime import datetime
from app.api.schemas import EmailStatsResponse
from app.db.session import get_db

class StatsService:
    def __init__(self, db):
        self.db = db
    
    def get_stats(self, date_from: datetime, date_to: datetime) -> EmailStatsResponse:
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