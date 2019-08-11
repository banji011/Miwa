import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from miwwa import mail 

def save_document(form_document):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_document.filename)
    document_fn = random_hex + f_ext
    document_path = os.path.join(current_app.root_path, 'static/docs/certs', document_fn)
    file = form_document
    file.save(document_path)
    return ('docs/certs/' + document_fn)



def save_profile_thumbnail(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/img/profile_pics', picture_fn)

    output_size=(150,150)

    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return ('img/profile_pics/' + picture_fn)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='MIWA Admin', recipients=[user.email] )
    msg.body = f''' To reset your password, visit the following link: 
    {url_for('main.reset_token',token=token,_external=True)}
    If you did not make this request, simply ignore this message and no changes will be made
    ''' 
    
    mail.send(msg) 