import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://toyuser:password@localhost/toy_store'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
