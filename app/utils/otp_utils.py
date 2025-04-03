import random
import string
from app.models.password_reset_token_model import PasswordResetToken
from app.database import db
from datetime import datetime, timezone
from flask import current_app

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def save_otp_to_db(email, otp):
    try:
        db.session.query(PasswordResetToken).filter_by(email=email).delete()

        new_otp = PasswordResetToken(email=email, otp=otp)
        db.session.add(new_otp)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False

def verify_otp(email, otp, used):
    try:
        otp_record = PasswordResetToken.query.filter_by(email=email, otp=otp).first()
    except Exception as e:
        return False

    if otp_record:
        print(current_app.config['TIME_ZONE'])

        expires_at_utc = otp_record.expires_at.replace(tzinfo=current_app.config['TIME_ZONE']) if otp_record.expires_at.tzinfo is None else otp_record.expires_at

        if datetime.now(current_app.config['TIME_ZONE']) < expires_at_utc:
            if(used == False):
                otp_record.is_verified = True
            elif(used and otp_record.is_verified == True):
                db.session.delete(otp_record)
            else:
                return False
            
            db.session.commit()
            return True
        else:
            db.session.delete(otp_record)
            db.session.commit()
            return False
    
    return False

