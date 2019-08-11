from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, IntegerField, HiddenField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from wtforms.fields.html5 import DateField 
from flask_wtf.file import FileField, FileAllowed 
from miwwa.models import *


class LoginForm(FlaskForm):
    phone  = StringField('Phone', validators=[DataRequired(), Length(min=10, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterPersonalForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = TextAreaField('Address ', validators=[DataRequired(), Length(min=10, max=200)])
    password = PasswordField('Choose Password', validators=[DataRequired(),Length(min=8, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    state_of_residence = SelectField('State of Residence',
                                    choices=[('Abia', 'Abia'),('Adamawa', 'Adamawa'),('Akwa Ibom', 'Akwa Ibom'),('Anambra', 'Anambra'),
                                            ('Bauchi', 'Bauchi'),('Bayelsa', 'Bayelsa'),('Benue', 'Benue'),('Borno', 'Borno'),
                                            ('Cross River', 'Cross River'),('Delta', 'Delta'),('Ebonyi', 'Ebonyi'),('Enugu', 'Enugu'),
                                            ('Edo', 'Edo'),('Ekiti', 'Ekiti'),('Gombe', 'Gombe'),('Imo', 'Imo'),
                                            ('Jigawa', 'Jigawa'),('Kaduna', 'Kaduna'),('Kano', 'Kano'),('Kastina', 'Kastina'),
                                            ('Kebbi', 'Kebbi'),('Kogi', 'Kogi'),('Kwara', 'Kwara'),('Lagos', 'Lagos'),
                                            ('Nasarawa', 'Nasarawa'),('Niger', 'Niger'),('Ogun', 'Ogun'),('Ondo', 'Ondo'),
                                            ('Osun', 'Osun'),('Oyo', 'Oyo'),('Plateau', 'Plateau'),('Rivers', 'Rivers'),
                                            ('Sokoto', 'Sokoto'),('Taraba', 'Taraba'),('Yobe', 'Yobe'),('Zamfara', 'Zamfara'),
                                            ('FCT', 'FCT')],validators=[DataRequired()])
    occupation = StringField('Occupation', validators=[DataRequired(), Length(min=2, max=20)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=2, max=20)])
    dob = DateField('Date of Birth',format='%Y-%m-%d')
    no_of_children = IntegerField('Number of Children', validators=[DataRequired()])
    area_of_interest = SelectField('Area of Interest', choices=[('Production', 'Production'),('Hairdressing', 'Hairdressing'),('Catering', 'Catering'),
                                        ('Baking', 'Baking'),('Tailoring', 'Tailoring'),('Computer Training', 'Computer Training'),
                                        ('Fishing', 'Fishing'),('Photography', 'Photography'),('Events & Decoration', 'Events & Decorations')],  validators=[DataRequired()])
    accept_toc = BooleanField('I have read and accepted the TOC ',validators=[DataRequired()] )
    submit = SubmitField('PROCEED')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('User with that email already exist, please use another email')

    def validate_phone(self, phone):
        user = User.query.filter_by(phone=phone.data).first()
        if user:
            raise ValidationError('User with that phone already exist, please use another phone')

class RegisterOfficerInfo(FlaskForm):
    service_number = StringField('Military Service Number', validators=[DataRequired(), Length(min=2, max=20)])
    first_name = StringField('Officer First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Officer Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    state_of_origin = SelectField('State of Origin',
                                    choices=[('Abia', 'Abia'),('Adamawa', 'Adamawa'),('Akwa Ibom', 'Akwa Ibom'),('Anambra', 'Anambra'),
                                            ('Bauchi', 'Bauchi'),('Bayelsa', 'Bayelsa'),('Benue', 'Benue'),('Borno', 'Borno'),
                                            ('Cross River', 'Cross River'),('Delta', 'Delta'),('Ebonyi', 'Ebonyi'),('Enugu', 'Enugu'),
                                            ('Edo', 'Edo'),('Ekiti', 'Ekiti'),('Gombe', 'Gombe'),('Imo', 'Imo'),
                                            ('Jigawa', 'Jigawa'),('Kaduna', 'Kaduna'),('Kano', 'Kano'),('Kastina', 'Kastina'),
                                            ('Kebbi', 'Kebbi'),('Kogi', 'Kogi'),('Kwara', 'Kwara'),('Lagos', 'Lagos'),
                                            ('Nasarawa', 'Nasarawa'),('Niger', 'Niger'),('Ogun', 'Ogun'),('Ondo', 'Ondo'),
                                            ('Osun', 'Osun'),('Oyo', 'Oyo'),('Plateau', 'Plateau'),('Rivers', 'Rivers'),
                                            ('Sokoto', 'Sokoto'),('Taraba', 'Taraba'),('Yobe', 'Yobe'),('Zamfara', 'Zamfara'),
                                            ('FCT', 'FCT')],validators=[DataRequired()])
    rank = StringField('Officer Rank', validators=[DataRequired(), Length(min=2, max=20)])
    dod = DateField('Date of Death',format='%Y-%m-%d')
    submit = SubmitField('PROCEED')


    def validate_service_number(self, service_number):
        officer = Officer.query.filter_by(service_no=service_number.data).first()
        if officer:
            raise ValidationError('Service Number already exist, Please check and try again')


class RegisterUploads(FlaskForm):
    death_cert = FileField('Upload Death Certificate', validators=[FileAllowed(['jpg','pdf','doc','docx'])])
    other = FileField('Profile Pics', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('REGISTER')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Email')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email, please register!')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class UpdateOneForm(FlaskForm):
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Proceed') 

    def validate_phone(self, phone):
        user = User.query.filter_by(phone=phone.data).first()
        if user is None:
            raise ValidationError('There is no account with that phone, please enter the correct phone number or register !')

class UpdatePersonalForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = TextAreaField('Address ', validators=[DataRequired(), Length(min=10, max=200)])
    password = PasswordField('Choose Password', validators=[DataRequired(),Length(min=8, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    state_of_residence = SelectField('State of Residence',
                                    choices=[('Abia', 'Abia'),('Adamawa', 'Adamawa'),('Akwa Ibom', 'Akwa Ibom'),('Anambra', 'Anambra'),
                                            ('Bauchi', 'Bauchi'),('Bayelsa', 'Bayelsa'),('Benue', 'Benue'),('Borno', 'Borno'),
                                            ('Cross River', 'Cross River'),('Delta', 'Delta'),('Ebonyi', 'Ebonyi'),('Enugu', 'Enugu'),
                                            ('Edo', 'Edo'),('Ekiti', 'Ekiti'),('Gombe', 'Gombe'),('Imo', 'Imo'),
                                            ('Jigawa', 'Jigawa'),('Kaduna', 'Kaduna'),('Kano', 'Kano'),('Kastina', 'Kastina'),
                                            ('Kebbi', 'Kebbi'),('Kogi', 'Kogi'),('Kwara', 'Kwara'),('Lagos', 'Lagos'),
                                            ('Nasarawa', 'Nasarawa'),('Niger', 'Niger'),('Ogun', 'Ogun'),('Ondo', 'Ondo'),
                                            ('Osun', 'Osun'),('Oyo', 'Oyo'),('Plateau', 'Plateau'),('Rivers', 'Rivers'),
                                            ('Sokoto', 'Sokoto'),('Taraba', 'Taraba'),('Yobe', 'Yobe'),('Zamfara', 'Zamfara'),
                                            ('FCT', 'FCT')],validators=[DataRequired()])
    occupation = StringField('Occupation', validators=[DataRequired(), Length(min=2, max=20)])
    dob = DateField('Date of Birth',format='%Y-%m-%d')
    no_of_children = IntegerField('Number of Children', validators=[DataRequired()])
    area_of_interest = SelectField('Area of Interest', choices=[('Production', 'Production'),('Hairdressing', 'Hairdressing'),('Catering', 'Catering'),
                                        ('Baking', 'Baking'),('Tailoring', 'Tailoring'),('Computer Training', 'Computer Training'),
                                        ('Fishing', 'Fishing'),('Photography', 'Photography'),('Events & Decoration', 'Events & Decorations')],  validators=[DataRequired()])
    accept_toc = BooleanField('I have read and accepted the TOC ',validators=[DataRequired()] )
    submit = SubmitField('PROCEED')


class UpdateOfficerForm(FlaskForm):
    service_number = StringField('Military Service Number', validators=[DataRequired(), Length(min=2, max=20)])
    first_name = StringField('Officer First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Officer Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    state_of_origin = SelectField('State of Origin',
                                    choices=[('Abia', 'Abia'),('Adamawa', 'Adamawa'),('Akwa Ibom', 'Akwa Ibom'),('Anambra', 'Anambra'),
                                            ('Bauchi', 'Bauchi'),('Bayelsa', 'Bayelsa'),('Benue', 'Benue'),('Borno', 'Borno'),
                                            ('Cross River', 'Cross River'),('Delta', 'Delta'),('Ebonyi', 'Ebonyi'),('Enugu', 'Enugu'),
                                            ('Edo', 'Edo'),('Ekiti', 'Ekiti'),('Gombe', 'Gombe'),('Imo', 'Imo'),
                                            ('Jigawa', 'Jigawa'),('Kaduna', 'Kaduna'),('Kano', 'Kano'),('Kastina', 'Kastina'),
                                            ('Kebbi', 'Kebbi'),('Kogi', 'Kogi'),('Kwara', 'Kwara'),('Lagos', 'Lagos'),
                                            ('Nasarawa', 'Nasarawa'),('Niger', 'Niger'),('Ogun', 'Ogun'),('Ondo', 'Ondo'),
                                            ('Osun', 'Osun'),('Oyo', 'Oyo'),('Plateau', 'Plateau'),('Rivers', 'Rivers'),
                                            ('Sokoto', 'Sokoto'),('Taraba', 'Taraba'),('Yobe', 'Yobe'),('Zamfara', 'Zamfara'),
                                            ('FCT', 'FCT')],validators=[DataRequired()])
    rank = StringField('Officer Rank', validators=[DataRequired(), Length(min=2, max=20)])
    dod = DateField('Date of Death',format='%Y-%m-%d')
    submit = SubmitField('PROCEED')


class UpdateUploadsForm(FlaskForm):
    death_cert = FileField('Upload Death Certificate', validators=[FileAllowed(['jpg','pdf','doc','docx'])])
    other = FileField('Profile Pics', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('REGISTER')


class ContactUsForm(FlaskForm):
    name =  StringField('Your Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=2, max=20)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=200)])
    submit = SubmitField('SEND MESSAGE')