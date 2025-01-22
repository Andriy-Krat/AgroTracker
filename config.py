import os
from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+pymysql://hayd:agro123*&back12@localhost:3306/agrotracker")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')  
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "vR3y!N9x#p$7tJf&dW*Z@4m8u^KbXzQY@!~3P")
    JWT_TOKEN_LOCATION = ["headers"]  # Токени будуть передаватися через заголовки
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

