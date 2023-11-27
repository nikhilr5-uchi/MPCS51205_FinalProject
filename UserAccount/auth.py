from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .models import User


auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.objects(email=email).first()

    if not user or user.password != password:
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) 

    login_user(user, remember=remember)
    print(f"Is Authenticated: {current_user.is_authenticated}")
    return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    
    if '@uchicago.edu' not in email:
        flash('Must sign up with @uchicago.edu email')
        return redirect(url_for('auth.signup'))

    user = User.objects(email=email).first()

    if user: 
        flash('Email address already exists. Go to login page')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, name=name, password=password)
    new_user.save()
    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))