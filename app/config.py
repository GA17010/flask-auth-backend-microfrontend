import os
from dotenv import load_dotenv
from datetime import timedelta
from pytz import timezone

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    JWT_SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_ACCESS_COOKIE_NAME = "accessToken"
    JWT_REFRESH_COOKIE_NAME = "refreshToken"
    JWT_COOKIE_CSRF_PROTECT = False

    EMAIL_FROM = os.getenv("EMAIL_FROM")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "").split(",")
    CORS_CREDENTIALS = True

    TIME_ZONE = timezone(os.getenv("TIME_ZONE"))