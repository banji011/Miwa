import os 
import secrets
from PIL import Image
from miwwa import  db, bcrypt
from flask import render_template, url_for, flash, redirect, request, session, g , Blueprint, current_app
from flask_login import login_user, current_user, logout_user, login_required
from miwwa.main.forms import * 
from sqlalchemy import desc
from sqlalchemy.sql import func
from miwwa.models import *
import uuid
from datetime import datetime, timedelta
from miwwa.main.utils import *
import requests 








main = Blueprint('main', __name__)




today = datetime.utcnow().strftime("%Y-%m-%d")


# def get_country(ip_address):
#     try:
#         response = requests.get(f"http://ip-api.com/json/{ip_address}")
#         js = response.json()
#         country = js['countryCode']
#         return country
#     except Exception as e:
#         return "Unknown"


@main.route('/',methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        current_app.logger.info(request.environ['REMOTE_ADDR'])
    else:
        current_app.logger.info(request.environ['HTTP_X_FORWARDED_FOR'])
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(phone=form.phone.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)
            if user.verified == False:
                return redirect(url_for('main.complete_reg'))
            return redirect(url_for('main.profile'))
        else:
            print('Phone or Password Incorrect')
            flash('Phone or Password Incorrect', 'warning')
    return render_template('main/index.html', title='Homepage', form=form)
    
 

 
@main.route('/profile') 
@login_required
def profile():
    user = User.query.filter_by(id=current_user.id).first()
    officer = Officer.query.filter_by(user_id=user.id).first()
    upload = Upload.query.filter_by(user_id=user.id).first()
    if user.verified == False:
        return redirect(url_for('main.complete_reg'))
    return render_template('main/profile.html', user=user,officer=officer,upload=upload)

@main.route('/register', methods=['GET','POST'])
def reg_personal():
    form = RegisterPersonalForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data,last_name=form.last_name.data,email=form.email.data,phone=form.phone.data,password=hashed_password,address=form.address.data,state_of_resident=form.state_of_residence.data,dob=form.dob.data,occupation=form.occupation.data,interest=form.area_of_interest.data,number_of_children=form.no_of_children.data)
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        requests.post(f"http://www.smsmobile24.com/index.php?option=com_spc&comm=spc_api&username=MZYF&password=MZYFS&sender=MIWA Admin&recipient={user.phone}&message= Thank You for creating a Miwa Account, Please complete your registration and get verified !  &")
        return redirect(url_for('main.reg_officer'))
    else:
        print(form.errors)
    return render_template('main/registerone.html', form=form)

@main.route('/register/officer',methods=['GET','POST'] )
def reg_officer():
    form = RegisterOfficerInfo()
    if form.validate_on_submit():
        user_id = session.get('user_id')
        user = User.query.filter_by(id=user_id).first() 
        print(user.first_name)
        inc_officer = Officer.query.filter_by(user_id=user_id).first()
        if inc_officer:
            inc_officer.first_name = form.first_name.data
            inc_officer.last_name = form.last_name.data
            inc_officer.state_of_origin = form.state_of_origin.data
            inc_officer.service_no = form.service_number.data
            inc_officer.rank = form.rank.data
            inc_officer.dod = form.dod.data
            db.session.commit()
        new_officer = Officer(first_name=form.first_name.data,last_name=form.last_name.data,state_of_origin=form.state_of_origin.data,service_no=form.service_number.data,rank=form.rank.data,dod=form.dod.data,user_id=user.id)
        db.session.add(new_officer)
        db.session.commit()
        return redirect(url_for('main.reg_upload'))
    else:
        print(form.errors)
    return render_template('main/registertwo.html', form=form)

@main.route('/register/uploads',methods=['GET','POST'] )
def reg_upload():
    form = RegisterUploads()
    if form.validate_on_submit():
        user_id = session.get('user_id')
        user = User.query.filter_by(id=user_id).first()
        print(user.first_name)
        if form.death_cert.data:
            death_cert = save_document(form.death_cert.data)
        if form.other.data:
            thumbnail = save_profile_thumbnail(form.other.data)
        inc_user_upload = Upload.query.filter_by(user_id=user_id).first()
        if inc_user_upload:
            inc_user_upload.death_cert = death_cert
            db.session.commit()
        new_upload = Upload(death_cert=death_cert,user_id=user.id)
        db.session.add(new_upload)
        user.thumbnail = thumbnail 
        user.verified = True
        user.verified_at = today
        db.session.commit()
        requests.post(f"http://www.smsmobile24.com/index.php?option=com_spc&comm=spc_api&username=MZYF&password=MZYFS&sender=MIWA Admin&recipient={user.phone}&message= Congratulations! Your Miwa account has been verified.  &")
        return redirect(url_for('main.acct_login'))
    return render_template('main/registerthree.html', form=form)


@main.route('/registration_successful')
def acct_login():
    return render_template('main/complete_reg.html', title='Account Created')


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@main.route('/reset_password', methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile')) 
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instruction to reset your password', 'info')
        return redirect(url_for('main.home'))
    return render_template('main/forgot-password.html', title='Reset Password',form=form)

@main.route('/reset_password/<token>', methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('main.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You can now login', 'success')
        return redirect(url_for('main.home'))
    return render_template('main/reset-password.html', title='Reset Password', form=form)



@main.route('/welcome_back',methods=['GET','POST'])
def update_one():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
    form = UpdateOneForm()
    if form.validate_on_submit():
        user = User.query.filter_by(phone=form.phone.data).first()
        if user.first_name is None:
            session['user_id'] = user.id
            return redirect(url_for('main.update_personal'))
        elif not user:
            flash('Please go and register, This page is mainly for account update !')
        else:
            flash('You are not allowed to edit here. Please request for password change', 'warning')
    return render_template('main/update_welcome.html',form=form,title='Welcome Back. Please Update your account ! ')

@main.route('/update_personal',methods=['GET','POST'])
def update_personal():
    form = UpdatePersonalForm()
    user_id = session.get('user_id')
    user = User.query.filter_by(id=user_id).first()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        user.password = hashed_password
        user.address = form.address.data
        user.state_of_resident = form.state_of_residence.data
        user.dob = form.dob.data
        user.occupation = form.occupation.data
        user.interest = form.area_of_interest.data
        user.number_of_children = form.no_of_children.data
        db.session.commit()
        return redirect(url_for('main.update_officer'))
    return render_template('main/update_registerone.html',form=form, user=user, title='Update Personal Details')

@main.route('/update_officer_info', methods=['GET','POST'])
def update_officer():
    form = UpdateOfficerForm()
    if form.validate_on_submit():
        user_id = session.get('user_id')
        user = User.query.filter_by(id=user_id).first()
        print(user.first_name)
        new_officer = Officer(first_name=form.first_name.data,last_name=form.last_name.data,state_of_origin=form.state_of_origin.data,service_no=form.service_number.data,rank=form.rank.data,dod=form.dod.data,user_id=user.id)
        db.session.add(new_officer)
        db.session.commit()
        return redirect(url_for('main.update_uploads'))
    else:
        print(form.errors)
    return render_template('main/update_registertwo.html', form=form, title='Update Officer Details ')

@main.route('/update_uploads',  methods=['GET','POST'])
def update_uploads():
    form = UpdateUploadsForm()
    if form.validate_on_submit():
        user_id = session.get('user_id')
        user = User.query.filter_by(id=user_id).first()
        print(user.first_name)
        if form.death_cert.data:
            death_cert = save_document(form.death_cert.data)
        if form.other.data:
            thumbnail = save_profile_thumbnail(form.other.data)
        
        new_upload = Upload(death_cert=death_cert,user_id=user.id)
        db.session.add(new_upload)
        user.thumbnail = thumbnail 
        db.session.commit()

        # requests.post(f"http://www.smsmobile24.com/index.php?option=com_spc&comm=spc_api&username=MZYF&password=MZYFS&sender=MIWA Admin&recipient={user.phone}&message= Congratulations! Your account has successfully been updated.  &")
        return redirect(url_for('main.acct_login'))
    return render_template('main/update_registerthree.html', form=form,title='Update Documents ')



@main.route('/incomplete_registration') 
@login_required
def complete_reg():
    user = User.query.filter_by(id=current_user.id).first()
    session['user_id'] = user.id
    return render_template('main/incomplete_reg.html', title='Complete Your Registration')

@main.route('/contactus',  methods=['GET','POST'])
def contact_us():
    form = ContactUsForm()
    if form.validate_on_submit():
        new_contact = ContactUs(name=form.name.data, email=form.email.data, phone=form.phone.data, message=form.message.data)
        db.session.add(new_contact)
        db.session.commit()
        msg = Message('NEW MESSAGE FROM MIWA', sender="MIWA Admin", recipients=['shola@imaginariumng.com','blessingajibero.ba@gmail.com'])
        msg.body = f'''
                Hello, 
                New massage from miwa reads:
                {form.message.data} 
                
                You can refer to Blessing for any further enquiries! 
         '''
        mail.send(msg)
        flash('Your message has been successfully sent !', 'success')
    else:
        print(form.errors)
    return render_template('main/contactus.html', form=form, title='Contact Us')


@main.route('/faqs')
def faqs():
    return render_template('main/faqs.html', title='Frequently asked questions')

@main.route('/aboutus')
def aboutus():
    return render_template('main/about.html', title='About Us')

@main.route('/events')
def events():
    return render_template('main/events.html', title='Upcoming events ')