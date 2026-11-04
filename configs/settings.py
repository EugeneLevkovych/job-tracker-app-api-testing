import os

BASE_URL = os.getenv("BASE_URL", "http://localhost:3050")
DEFAULT_USER_EMAIL = os.getenv("DEFAULT_USER_EMAIL","student@example.com")
DEFAULT_USER_PASSWORD = os.getenv("DEFAULT_USER_PASSWORD","Password123!")