from starlette.config import Config
from starlette.datastructures import URL, Secret


config = Config(".env")

TESTING = config('TESTING', cast=bool, default=False)

SECRET_KEY = config("SECRET_KEY", cast=str, default=False)

FRONTEND_BASE_URL = config("FRONTEND_BASE_URL", cast=str, default="")
LOGIN_URL_PATH = config("LOGIN_URL_PATH", cast=str, default="/login")

EMAIL_TOKEN_EXPIRE_MINUTES = config("EMAIL_TOKEN_EXPIRE_MINUTES", cast=int, default=30)
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=30)

SMTP_HOST = config("SMTP_HOST", cast=str, default=False)
SMTP_PORT = config("SMTP_PORT", cast=str, default=False)
SMTP_USERNAME = config("SMTP_USERNAME", cast=str, default=False)
SMTP_PASSWORD = config("SMTP_PASSWORD", cast=str, default=False)

STRIPE_API_SECRET = config("STRIPE_API_SECRET", cast=str, default=False)
STRIPE_DEFAULT_PLAN_ID = config("STRIPE_DEFAULT_PLAN_ID", cast=str, default=False)