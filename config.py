import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+pymysql://hayd:agro123*&back12@localhost:3306/agrotracker")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
