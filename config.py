import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+pymysql://hayd:agro123*&back12@localhost:3306/agrotracker")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')  
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  
