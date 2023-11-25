from flask import Blueprint, render_template
# from . import db
import pymongo

main = Blueprint('main', __name__)

# Database

# client = pymongo.MongoClient('localhost', 27017)

# db = client.user_login_system

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
def profile():
    return render_template('profile.html')