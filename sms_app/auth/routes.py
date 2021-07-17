from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.urls import url_parse

from sms_app.auth import bp
from sms_app.auth.forms import LoginForm, RegisterForm, ResetPasswordRequestForm, ResetPasswordForm
from sms_app.auth.email import send_password_reset_email, send_verify_email

from sms_app.models import User
from sms_app.tokens import confirm_token
from sms_app.decorators import check_confirmed

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        if User.register(email=email, password=form.password.data):
            flash('Account created for {}'.format(email), 'success')
            send_verify_email(email)
            login_user(User.get_by_email(email))
            return redirect(url_for('auth.unconfirmed'))
    return render_template('auth/register.html', title='Register', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        if User.login_valid(email, form.password.data):
            user = User.get_by_email(email)
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('main.index')
            return redirect(next_page)
        flash('Invalid email or password')
        return redirect(url_for('auth.login'))
    return render_template('auth/login.html', title='Log In', form=form)

@bp.route('/logout')
def logout():
    try:
        logout_user()
    except:
        pass
    return redirect(url_for('main.index'))

@bp.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.verified:
        return redirect(url_for('main.index'))
    flash('Please confirm your account!', 'warning')
    return render_template('auth/unconfirmed.html', title='Unconfirmed')

@bp.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.get_by_email(email=email)
    if user.verified:
        flash('Account already confirmed. Please login.', 'success')
    else:
        User.verify(email)
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('main.index'))

@bp.route('/resend')
@login_required
def resend_confirmation():
    send_verify_email(current_user.email)
    flash('A new confirmation email has been sent.', 'success')
    return redirect(url_for('auth.unconfirmed'))

@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data.lower())
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html', title='Reset Password', form=form)

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.reset_password(form.password.data)
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', title='Reset Password' ,form=form)
