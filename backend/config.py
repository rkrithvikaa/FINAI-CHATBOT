import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    # Flask secret key
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "finai-super-secret-key-2026-change-this"
    )

    # JWT secret key
    # Must be long enough for HS256
    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "finai-jwt-super-secret-key-2026-very-secure"
    )

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///finai.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False