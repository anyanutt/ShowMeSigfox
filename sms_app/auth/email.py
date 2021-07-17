from flask import render_template, url_for, current_app

from sms_app import mail
from sms_app.email import send_email
from sms_app.tokens import generate_confirmation_token

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('ShowMeSigfox - Reset Your Password',
               sender=current_app.config['MAIL_USERNAME'],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))

def send_verify_email(email):
    token = generate_confirmation_token(email)
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    send_email('ShowMeSigfox - Account Verification',
               sender=current_app.config['MAIL_USERNAME'],
               recipients=[email],
               text_body=render_template('email/verify.txt', confirm_url=confirm_url),
               html_body=render_template('email/verify.html', confirm_url=confirm_url))
