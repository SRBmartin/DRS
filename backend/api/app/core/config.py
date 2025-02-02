import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    EMAIL_SERVICE_URL = os.environ.get('EMAIL_SERVICE_URL', 'http://localhost:5569/mail/send')
    EMAIL_SERVICE_API = os.getenv('EMAIL_SERVICE_API', 'f1b4b3b1-1b1b-4b1b-8b1b-1b1b1b1b1b1b')
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:4200')