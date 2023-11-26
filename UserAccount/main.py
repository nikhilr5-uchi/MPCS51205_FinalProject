from flask import Blueprint, render_template, redirect, url_for
# from . import db
import pymongo

main = Blueprint('main', __name__)

# Database

# client = pymongo.MongoClient('localhost', 27017)

# db = client.user_login_system

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/home')
def home():
    return render_template('home.html')

@main.route('/search')
def search():
    # Add logic for handling the search here
    return render_template('search_results.html')

@main.route('/all_listings')
def all_listings():
    return render_template('all_listings.html')

@main.route('/add_listing')
def add_listing():
    return render_template('add_listing.html')

@main.route('/shopping_cart')
def shopping_cart():
    return render_template('shopping_cart.html')

@main.route('/profile')
def profile():
    return render_template('profile.html')