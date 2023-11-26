from flask import Blueprint, render_template, redirect, url_for, request
# from . import db
import pymongo

main = Blueprint('main', __name__) 

# Database

# client = pymongo.MongoClient('localhost', 27017)

# db = client.user_login_system

# Sample user data
sample_user = {
    'email': 'sample@example.com',
    'name': 'John Doe',
    'address': '123 Main St, Cityville',
    'orders': [
        {'id': 1, 'product_name': 'Product 1'},
        {'id': 2, 'product_name': 'Product 2'},
    ]
}

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
    new_address = request.args.get('new_address')
    return render_template('profile.html', user=sample_user, new_address=new_address)

@main.route('/edit_address')
def edit_address():
    # Render a form to edit the address
    return render_template('edit_address.html', user=sample_user)

@main.route('/save_address', methods=['POST'])
def save_address():
    current_address = request.form.get('current_address')
    new_address = request.form.get('new_address')

    # Update the user's address in your data store

    return redirect(url_for('main.profile', new_address=new_address))

@main.route('/order_details/<int:order_id>')
def order_details(order_id):
    # Fetch order details based on order_id
    # For simplicity, using a sample order dictionary
    order = {'id': order_id, 'product_name': f'Product {order_id}'}
    return render_template('order_details.html', order=order)

