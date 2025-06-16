from .base import BaseConfig
import os

class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("PROD_DATABASE_URL")
    CORS_ORIGINS = [os.getenv("CLIENT_URL"), os.getenv("CLIENT_URL_2")]