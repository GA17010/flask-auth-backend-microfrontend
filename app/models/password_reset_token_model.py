from datetime import datetime, timedelta
from app.database import db
import pytz

class PasswordResetToken(db.Model):
    __tablename__ = "password_reset_tokens"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False, index=True)
    otp = db.Column(db.String(6), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('America/El_Salvador'))) 
    expires_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, email, otp):
        self.email = email
        self.otp = otp
        self.expires_at = datetime.now(pytz.timezone('America/El_Salvador')) + timedelta(minutes=10)

    def is_expired(self):
        return datetime.now(pytz.timezone('America/El_Salvador')) > self.expires_at
