import os 
from datetime import timedelta

class Config:
    SECRET_KEY =  '5791628bb0b13ce0c676dfde280ba895'
    SQLALCHEMY_DATABASE_URI =  'sqlite:///miwwa_project.db' 
    PERMANENT_SESSION_LIFETIME =  timedelta(minutes=30)
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True 
    MAIL_USERNAME = 'ola.banjy@gmail.com'
    MAIL_PASSWORD = '07065907455'