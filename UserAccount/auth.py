from flask import Blueprint, render_template, redirect, url_for

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/logout')
def logout():
    return render_template('logout.html')

@auth.route('/process-login', methods=['POST'])
def process_login():
    # Process login logic here

    # Redirect to the main.index route after successful login
    return redirect(url_for('main.all_listings'))
