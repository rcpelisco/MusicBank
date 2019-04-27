from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user
from web_app import db, bcrypt
from web_app.models import User
from web_app.users.forms import RegistrationForm, LoginForm

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, name=form.name.data, password=hashed)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! You can now log in.', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', 
        title='Register', 
        form=form)
        
@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    hashed = bcrypt.generate_password_hash('pass').decode('utf-8')
    print(bcrypt.check_password_hash(hashed, 'pass'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.index'))
        else: 
            flash('Login Unsucccessful. Please check username and/or password.', 'danger')
    return render_template('login.html', 
        title='Login', 
        form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
