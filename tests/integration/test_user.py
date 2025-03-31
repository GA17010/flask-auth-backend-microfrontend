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
    "email": "testuser1@example.com",
    "password": "Password@123",
    "confirm_password": "Password@123"
  }


def test_get_users_empty(client):
  response = client.get("/user/users")
  
  assert response.status_code == 200
  assert response.json == []

def test_get_users_with_data(client, new_user):
  client.post("/auth/register", json=new_user)
  response = client.get("/user/users")

  assert response.status_code == 200
  assert len(response.json) == 1
  assert response.json[0]["full_name"] == new_user["full_name"]
  assert response.json[0]["email"] == new_user["email"]

def test_delete_user(client, new_user):
  register_response = client.post("/auth/register", json=new_user)
  assert register_response.status_code == 201
  
  response = client.get("/user/users")
  assert response.status_code == 200
  assert len(response.json) == 1

  user = response.json[0]
  assert "id" in user, f"La respuesta no contiene 'id': {response.json}"
  user_id = user["id"]

  delete_response = client.delete(f"/user/users/{user_id}")
  assert delete_response.status_code == 200
  assert "data" in delete_response.json, f"Respuesta inesperada: {delete_response.json}"
  assert delete_response.json["data"]["message"] == "Usuario eliminado exitosamente"

  response_after_delete = client.get("/user/users")
  assert response_after_delete.status_code == 200
  assert response_after_delete.json == []
