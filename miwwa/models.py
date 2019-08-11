from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer 
from flask import current_app
from miwwa import db, login_manager
from flask_login import UserMixin 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100),unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    state_of_resident = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(100), nullable=False)
    occupation = db.Column(db.String(100), nullable=False)
    interest =  db.Column(db.String(100), nullable=False)
    thumbnail = db.Column(db.String(255), nullable=False,default="thubmnail.jpg")
    number_of_children = db.Column(db.String(100), nullable=False,default=0)
    signed_up_at = db.Column(db.DateTime(), default=datetime.utcnow)
    verified = db.Column(db.Boolean, unique=False, default=False)
    verified_at = db.Column(db.String(100), nullable=False,default="Not Verified")
    officer = db.relationship('Officer', backref='users', lazy=True)
    uploads = db.relationship('Upload', backref='users', lazy=True)
    children = db.relationship('Children', backref='users', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None 
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.first_name}','{self.last_name}','{self.phone}', '{self.thumbnail}')"


class Officer(db.Model):
    __tablename__ = 'officers'
    id = db.Column(db.Integer, primary_key=True)
    first_name =  db.Column(db.String(100), nullable=False)
    last_name =  db.Column(db.String(100), nullable=False)
    state_of_origin = db.Column(db.String(100), nullable=False)
    service_no =  db.Column(db.String(100), nullable=False)
    rank =  db.Column(db.String(100), nullable=False)
    dod =  db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    user = db.relationship('User', backref='user_officers', foreign_keys=[user_id])

class Upload(db.Model):
    __tablename__ = 'uploads'
    id = db.Column(db.Integer, primary_key=True)
    cv = db.Column(db.String(255), nullable=True)
    death_cert = db.Column(db.String(255), nullable=True)
    insurance_doc = db.Column(db.String(255), nullable=True)
    driver_license = db.Column(db.String(255), nullable=True)
    national_id = db.Column(db.String(255), nullable=True)
    int_passport = db.Column(db.String(255), nullable=True)
    others = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    user = db.relationship('User', backref='user_uploads', foreign_keys=[user_id])

class Children(db.Model):
    __tablename__ = 'children'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    user = db.relationship('User', backref='user_children', foreign_keys=[user_id])

    
class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    thumbnail = db.Column(db.String(100), nullable=False, default="defaultimg.jpg")

    def __repr__(self):
        return f"User('{self.name}','{self.email}','{self.role}', '{self.thumbnail}')"

class ContactUs(db.Model):
    __tablename__ = 'contactus'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(255), nullable=False)