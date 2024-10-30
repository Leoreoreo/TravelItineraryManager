# app/config.py
import os
from dotenv import load_dotenv

# load environment variables from the .env file
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'f3cfe9ed9fae319fe2024dbf')
    DB_USERNAME = os.getenv('DB_USERNAME', 'db_user1') 
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'tim$1234$') 
    DB_HOST = os.getenv('DB_HOST', '18.222.124.5')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'tim_db') 

    #SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
    #SQLALCHEMY_TRACK_MODIFICATIONS = False

    #SQLALCHEMY_DATABASE_URI = 'postgresql://db_user1:your_password@your_ec2_ip:5432/tim_db'
    #SQLALCHEMY_TRACK_MODIFICATIONS = False
