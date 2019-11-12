import os

SESSION_COOKIE_NAME = 'session'
SESSION_COOKIE_PATH = '/'
SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_ENABLED = False
UPLOAD_DIR = 'static/upload'

SENTRY_DSN = os.environ.get("SENTRY_DSN")

POSTGRES_USER = os.environ.get("POSTGRES_USER", 'postgres')
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", 'hg56LK76h0')
POSTGRES_DB = os.environ.get("POSTGRES_DB", 'indoor')
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", 'indoor-db')
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", '5432')
DATABASE_URL = f'{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DATABASE_URL}'

SECRET_KEY = os.environ.get("SECRET_KEY", "WERTGbhygF#$%^&*(*&^%$EDFGBN")

SERVER_NAME = os.environ.get("SERVER_NAME")
SESSION_COOKIE_DOMAIN = SERVER_NAME

REDIS_HOST = os.environ.get("REDIS_HOST", "indoor-redis")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)

AUTH_COOKIE_NAME = os.environ.get("AUTH_COOKIE_NAME", 'SID')
