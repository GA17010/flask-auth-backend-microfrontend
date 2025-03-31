import jwt
import pytest
from unittest.mock import patch
from app.utils.jwt_utils import verify_token

class DummyConfig:
  SECRET_KEY = "dummy_secret"

@pytest.fixture(autouse=True)
def set_dummy_config(monkeypatch):
  # Simula que current_app.config contiene dummy config
  monkeypatch.setattr("app.utils.jwt_utils.current_app", type("Dummy", (), {"config": DummyConfig.__dict__}))

# ✅ Prueba: Validación de token correcto
def test_verify_token_success():
  token = "dummy_token"
  dummy_payload = {"type": "access", "id": 1}
  
  with patch("app.utils.jwt_utils.jwt.decode", return_value=dummy_payload):
    payload, error = verify_token(token, "access")
    
    assert error is None
    assert payload == dummy_payload

# ❌ Prueba: Error si el tipo de token es incorrecto
def test_verify_token_invalid_type():
  token = "dummy_token"
  dummy_payload = {"type": "refresh", "id": 1}
  
  with patch("app.utils.jwt_utils.jwt.decode", return_value=dummy_payload):
    payload, error = verify_token(token, "access")

    assert payload is None
    assert error == "Tipo de token inválido"

# ❌ Prueba: Error si el Token es incorrecto
def test_verify_token_invalid_token():
  token = "dummy_token"
  
  with patch("app.utils.jwt_utils.jwt.decode", side_effect=jwt.InvalidTokenError):
    payload, error = verify_token(token, "access")

    assert payload is None
    assert error == "Token inválido"
