import pytest
from app import create_app
from app.database import db

@pytest.fixture
def app():
  app = create_app()
  app.config.update({
    "TESTING": True,
    "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    "SECRET_KEY": "test_secret_key",
  })

  with app.app_context():
    db.create_all()
    yield app
    db.session.remove()
    db.drop_all()

@pytest.fixture
def client(app):
  return app.test_client()

@pytest.fixture
def new_user():
  return {
    "full_name": "Test User",
    "email": "testuser@example.com",
    "password": "Password@123",
    "confirm_password": "Password@123"
  }

def test_register_user(client, new_user):
  response = client.post("/auth/register", json=new_user)
  assert response.status_code == 201
  assert response.json["data"]["message"] == "Registrado exitosamente"

def test_register_user_existing_email(client, new_user):
  client.post("/auth/register", json=new_user)
  response = client.post("/auth/register", json=new_user)
  assert response.status_code == 409
  assert response.json["data"]["message"] == "El usuario ya existe"

def test_register_user_invalid_password(client):
  invalid_user = {
    "full_name": "Test User",
    "email": "testuser@example.com",
    "password": "weakpass",
    "confirm_password": "weakpass"
  }
  response = client.post("/auth/register", json=invalid_user)
  assert response.status_code == 400
  assert "Datos invalidos" in response.json["data"]["message"]

def test_register_user_password_mismatch(client):
  invalid_user = {
    "full_name": "Test User",
    "email": "testuser@example.com",
    "password": "weakpass@123",
    "confirm_password": "weakpass@456"
  }
  response = client.post("/auth/register", json=invalid_user)
  assert response.status_code == 400
  assert "Datos invalidos" in response.json["data"]["message"]

def test_register_user_missing_fields(client):
  incomplete_user = {
    "full_name": "Test User",
    "password": "Password@123",
    "confirm_password": "Password@123"
  }
  response = client.post("/auth/register", json=incomplete_user)
  assert response.status_code == 400
  assert "Datos invalidos" in response.json["data"]["message"]


def test_login_user(client, new_user):
  client.post("/auth/register", json=new_user)
  login_data = {
    "email": new_user["email"],
    "password": new_user["password"]
  }
  response = client.post("/auth/login", json=login_data)
  assert response.status_code == 200
  assert response.json["data"]["message"] == "Autenticado exitosamente"

def test_login_user_invalid_credentials(client, new_user):
  client.post("/auth/register", json=new_user)
  login_data = {
    "email": new_user["email"],
    "password": "WrongPassword@123"
  }
  response = client.post("/auth/login", json=login_data)
  assert response.status_code == 401
  assert response.json["data"]["message"] == "Credenciales incorrectas"

def test_login_user_missing_fields(client, new_user):
  client.post("/auth/register", json=new_user)
  login_data = {"email": new_user["email"]}
  response = client.post("/auth/login", json=login_data)
  assert response.status_code == 400
  assert "Datos invalidos" in response.json["data"]["message"]


def test_check_auth(client, new_user):
  client.post("/auth/register", json=new_user)
  login_data = {
    "email": new_user["email"],
    "password": new_user["password"]
  }

  login_response = client.post("/auth/login", json=login_data)

  cookie_header = login_response.headers.get("Set-Cookie")
  access_token = cookie_header.split("accessToken=")[1].split(";")[0]

  client.set_cookie("accessToken", access_token, domain="localhost" )
  response = client.get("/auth/checkAuth")
  assert response.status_code == 200
  assert response.json["data"]["message"] == "Token valido"

def test_check_auth_invalid_token(client):
  client.set_cookie("accessToken", "invalid_token", domain="localhost" )
  response = client.get("/auth/checkAuth")

  assert response.status_code == 401
  assert response.json["data"]["message"] == "Token inválido"


def test_refresh_token(client, new_user):
  client.post("/auth/register", json=new_user)
  login_data = {
    "email": new_user["email"],
    "password": new_user["password"]
  }
  login_response = client.post("/auth/login", json=login_data)

  cookie_headers = login_response.headers.getlist("Set-Cookie")
  refresh_token = None
  for cookie in cookie_headers:
    if "refreshToken=" in cookie:
      refresh_token = cookie.split("refreshToken=")[1].split(";")[0]
      break
  assert refresh_token is not None, "No se encontró refresh token en las cookies"

def test_refresh_token_invalid(client):
  client.set_cookie("refreshToken", "invalid_token", domain="localhost")
  response = client.post("/auth/refreshToken")

  assert response.status_code == 401
  assert "Token inválido" in response.json["data"]["message"]

def test_logout_user(client, new_user):
  client.post("/auth/register", json=new_user)
  login_data = {
    "email": new_user["email"],
    "password": new_user["password"]
  }
  client.post("/auth/login", json=login_data)
  response = client.post("/auth/logout")
  assert response.status_code == 200
  assert response.json["data"]["message"] == "Seccion Cerrada"


def test_logout_without_login(client):
  response = client.post("/auth/logout")
  assert response.status_code == 200
  assert response.json["data"]["message"] == "Seccion Cerrada"

def test_refresh_token_user_agent_mismatch(client, new_user):
  client.post("/auth/register", json=new_user)
  login_data = {
    "email": new_user["email"],
    "password": new_user["password"]
  }
  login_response = client.post("/auth/login", json=login_data)
  
  cookie_headers = login_response.headers.getlist("Set-Cookie")
  refresh_token = None
  for cookie in cookie_headers:
    if "refreshToken=" in cookie:
      refresh_token = cookie.split("refreshToken=")[1].split(";")[0]
      break
  assert refresh_token is not None, "No se encontró refresh token en las cookies"
  
  response = client.post(
    "/auth/refreshToken", 
    headers={"Cookie": f"refreshToken={refresh_token}", "User-Agent": "OtroUserAgent/1.0"}
  )
  
  assert response.status_code == 403
  assert "User-Agent no coincide" in response.json["data"]["message"]
