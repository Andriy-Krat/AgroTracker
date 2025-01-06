import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+pymysql://hayd:agro123*&back12@localhost:3306/agrotracker")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')  
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  
    MAILGUN_DOMAIN = "sandbox38d99722ff5b4dbf8bd889f428084e7f.mailgun.org"
    MAILGUN_API_KEY = "22471c836093fe58ef296638b0e30b76-e61ae8dd-48d2b7c8"  
