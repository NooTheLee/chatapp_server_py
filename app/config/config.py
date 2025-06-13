import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET = os.getenv("JWT_SECRET")
    JWT_ISSUER = os.getenv("JWT_ISSUER")
    JWT_AUDIENCE = os.getenv("JWT_AUDIENCE")
    JWT_EXPIRES_HOURS = os.getenv("JWT_EXPIRES_HOURS", 12)
    SECRET_KEY = os.getenv("SECRET_KEY")
