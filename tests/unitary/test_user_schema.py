import pytest
from marshmallow import ValidationError
from app.schemas.user_schema import UserSchema, RegistrationSchema, LoginSchema

@pytest.fixture
def user_schema():
  return UserSchema()

@pytest.fixture
def registration_schema():
  return RegistrationSchema()

@pytest.fixture
def login_schema():
  return LoginSchema()

# ✅ Prueba: Validación de datos correctos
def test_valid_user_data(user_schema):
  valid_data = {
    "full_name": "John Doe",
    "company": "Tech Corp",
    "password": "Secure@123",
    "email": "john@example.com"
  }
  result = user_schema.load(valid_data)
  assert result["full_name"] == "John Doe"
  assert result["email"] == "john@example.com"

# ❌ Prueba: Error si falta un campo requerido
def test_missing_required_field(user_schema):
  invalid_data = {
    "company": "Tech Corp",
    "password": "Secure@123"
  }
  with pytest.raises(ValidationError) as excinfo:
    user_schema.load(invalid_data)
  
  assert "full_name" in excinfo.value.messages
  assert "email" in excinfo.value.messages

# ❌ Prueba: Error si el email es inválido
def test_invalid_email(user_schema):
  invalid_data = {
    "full_name": "John Doe",
    "company": "Tech Corp",
    "password": "Secure@123",
    "email": "invalid-email"
  }
  with pytest.raises(ValidationError) as excinfo:
    user_schema.load(invalid_data)
  
  assert "email" in excinfo.value.messages

# ❌ Prueba: Error si la contraseña no tiene mayúscula
def test_password_without_uppercase(user_schema):
  invalid_data = {
    "full_name": "John Doe",
    "company": "Tech Corp",
    "password": "secure@123",
    "email": "john@example.com"
  }
  with pytest.raises(ValidationError) as excinfo:
    user_schema.load(invalid_data)

  assert "The password must contain at least one capital letter." in excinfo.value.messages["password"]

# ❌ Prueba: Error si la contraseña no tiene un carácter especial
def test_password_without_special_char(user_schema):
  invalid_data = {
    "full_name": "John Doe",
    "company": "Tech Corp",
    "password": "Secure123",
    "email": "john@example.com"
  }
  with pytest.raises(ValidationError) as excinfo:
    user_schema.load(invalid_data)

  assert "The password must contain at least one of the following characters: @#$%&" in excinfo.value.messages["password"]

# ✅ Prueba: Registro con confirmación de contraseña correcta
def test_registration_valid_data(registration_schema):
  valid_data = {
    "full_name": "John Doe",
    "company": "Tech Corp",
    "password": "Secure@123",
    "confirm_password": "Secure@123",
    "email": "john@example.com"
  }
  result = registration_schema.load(valid_data)
  assert result["password"] == "Secure@123"

# ❌ Prueba: Error si las contraseñas no coinciden en el registro
def test_registration_password_mismatch(registration_schema):
  invalid_data = {
    "full_name": "John Doe",
    "company": "Tech Corp",
    "password": "Secure@123",
    "confirm_password": "Secure@456",
    "email": "john@example.com"
  }
  with pytest.raises(ValidationError) as excinfo:
    registration_schema.load(invalid_data)

  assert "confirm_password" in excinfo.value.messages  # No pasará la validación si no coinciden

# ✅ Prueba: Validación de inicio de sesión correcto
def test_valid_login_data(login_schema):
  valid_data = {
    "email": "john@example.com",
    "password": "Secure@123"
  }
  result = login_schema.load(valid_data)
  assert result["email"] == "john@example.com"

# ❌ Prueba: Error si falta email en login
def test_missing_email_in_login(login_schema):
  invalid_data = {
    "password": "Secure@123"
  }
  with pytest.raises(ValidationError) as excinfo:
    login_schema.load(invalid_data)

  assert "email" in excinfo.value.messages
