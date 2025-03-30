import pytest
from flask import Flask
from app import create_app
from app.database import db
from app.models.user_model import User

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
    "full_name": "Test User1",
    "email": "testuser@example.com",
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
  print(response.json)
  assert response.status_code == 200
  assert len(response.json) == 1
  assert response.json[0]["full_name"] == new_user["full_name"]
  assert response.json[0]["email"] == new_user["email"]

