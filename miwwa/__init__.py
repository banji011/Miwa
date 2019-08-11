import os 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
from flask_mail import Mail
from datetime import timedelta
from flask_login import LoginManager 
from miwwa.config import Config
import logging

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'main.home'
login_manager.login_message_category = 'warning'
mail = Mail()
logging.basicConfig(filename='mylog.txt',
                    level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s"
                    )

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)




    from miwwa.main.routes import main
    from miwwa.errors.handlers import errors
    from miwwa.admin.routes import admin
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(admin)
    

    return app 




