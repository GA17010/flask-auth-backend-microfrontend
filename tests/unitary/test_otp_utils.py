import pytest
from unittest.mock import patch, MagicMock
from app.utils.otp_utils import generate_otp, save_otp_to_db, verify_otp
from app.models.password_reset_token_model import PasswordResetToken
from datetime import datetime, timedelta
from app import create_app
from pytz import timezone

@pytest.fixture
def mock_db_session():
  with patch("app.utils.otp_utils.db.session") as mock_session:
    yield mock_session

@pytest.fixture
def mock_password_reset_token():
  with patch("app.utils.otp_utils.PasswordResetToken") as mock_model:
    yield mock_model

@pytest.fixture
def mock_current_app():
  app = create_app()
  with app.app_context():
    with patch.dict(app.config, {"TIME_ZONE": timezone('America/El_Salvador')}):
      yield app


# ✅ Test: Generate OTP
def test_generate_otp():
  otp = generate_otp()
  assert len(otp) == 6
  assert otp.isdigit()

# ✅ Test: Save OTP to DB
def test_save_otp_to_db(mock_db_session, mock_password_reset_token):
  email = "test@example.com"
  otp = "123456"

  save_otp_to_db(email, otp)

  mock_db_session.query().filter_by.assert_called_with(email=email)
  mock_db_session.query().filter_by().delete.assert_called_once()
  mock_password_reset_token.assert_called_with(email=email, otp=otp)
  mock_db_session.add.assert_called_once()
  mock_db_session.commit.assert_called_once()

# ✅ Test: Verify OTP - Valid OTP
def test_verify_otp_valid(mock_password_reset_token, mock_db_session, mock_current_app):
  email = "test@example.com"
  otp = "123456"
  mock_record = MagicMock()
  mock_record.expires_at = datetime.now() + timedelta(minutes=5)
  mock_password_reset_token.query.filter_by.return_value.first.return_value = mock_record

  result = verify_otp(email, otp, used=False)

  assert result is True
  assert mock_record.is_verified is True
  mock_db_session.commit.assert_called_once()

# ❌ Test: Verify OTP - Expired OTP
def test_verify_otp_expired(mock_password_reset_token, mock_db_session, mock_current_app):
  email = "test@example.com"
  otp = "123456"
  mock_record = MagicMock()
  mock_record.expires_at = datetime.now() - timedelta(minutes=5)
  mock_password_reset_token.query.filter_by.return_value.first.return_value = mock_record

  result = verify_otp(email, otp, used=False)

  assert result is False
  mock_db_session.delete.assert_called_once_with(mock_record)
  mock_db_session.commit.assert_called_once()

# ❌ Test: Verify OTP - Invalid OTP
def test_verify_otp_invalid(mock_password_reset_token):
  email = "test@example.com"
  otp = "123456"
  mock_password_reset_token.query.filter_by.return_value.first.return_value = None

  result = verify_otp(email, otp, used=False)

  assert result is False

# ✅ Test: Verify OTP - Used OTP
def test_verify_otp_used(mock_password_reset_token, mock_db_session, mock_current_app):
  email = "test@example.com"
  otp = "123456"
  mock_record = MagicMock()
  mock_record.expires_at = datetime.now() + timedelta(minutes=5)
  mock_record.is_verified = True
  mock_password_reset_token.query.filter_by.return_value.first.return_value = mock_record

  result = verify_otp(email, otp, used=True)

  assert result is True
  mock_db_session.delete.assert_called_once_with(mock_record)
  mock_db_session.commit.assert_called_once()

# ✅ Test: Verify OTP - No OTP Record Found
def test_verify_otp_no_record(mock_password_reset_token):
  email = "test@example.com"
  otp = "123456"

  mock_password_reset_token.query.filter_by.return_value.first.return_value = None

  result = verify_otp(email, otp, used=False)

  assert result is False 

# ✅ 4. Test: Verify OTP - Expired But Not Deleted
def test_verify_otp_expired_cleanup(mock_password_reset_token, mock_db_session, mock_current_app):
  email = "test@example.com"
  otp = "123456"
  mock_record = MagicMock()
  mock_record.expires_at = datetime.now() - timedelta(minutes=5)  # Expirado
  mock_password_reset_token.query.filter_by.return_value.first.return_value = mock_record

  result = verify_otp(email, otp, used=False)

  assert result is False
  mock_db_session.delete.assert_called_once_with(mock_record)  # OTP expirado debe eliminarse
  mock_db_session.commit.assert_called_once()
