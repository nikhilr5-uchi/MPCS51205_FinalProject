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
        {
            'id': 1,
            'product_name': 'College Math',
            'image': 'math_textbook.jpg', 
            'price': 12.0,
            'buy_now_enabled': True, 
            'bid_won': False
        },
        {
            'id': 2,
            'product_name': 'College Dictionary of Psychology',
            'image': 'psychology.jpeg', 
            'price': 15.0,
            'buy_now_enabled': False, 
            'bid_won': True
        },
        # Add more orders as needed
    ],
    'listings': [
        {
            'id': 1,
            'product_title': 'Desk Lamp',
            'image': 'lamp.jpg',
            'min_bid': 5.0,
            'expiration_date': '2023-12-31',
            'location': 'Hyde Park',
            'description': 'Desk Lamp used for 5 months.',
            'buy_now_enabled': True,
        },
        {
            'id': 2,
            'product_title': 'Study Table',
            'image': 'table.jpg',
            'min_bid': 70.0,
            'expiration_date': '2023-12-30',
            'location': 'Hyde Park',
            'description': 'Study Table used for 1 month.',
            'buy_now_enabled': False,
        },
        # Add more listings as needed
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
    return render_template('all_listings.html', user=sample_user)

@main.route('/add_listing')
def add_listing():
    return render_template('add_listing.html')

@main.route('/shopping_cart')
def shopping_cart():
    return render_template('shopping_cart.html', user=sample_user)

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

@main.route('/product_details/<int:listing_id>')
def product_details(listing_id):
    listing = next((listing for listing in sample_user['listings'] if listing['id'] == listing_id), None)
    if listing:
        return render_template('product_details.html', listing=listing)
    else:
        # Handle listing not found
        return redirect(url_for('main.my_listings'))

@main.route('/my_listings')
def my_listings():
    return render_template('my_listings.html', user=sample_user)

@main.route('/place_bid/<int:listing_id>', methods=['POST'])
def place_bid(listing_id):
    # Fetch the listing from the user's data
    listing = next((listing for listing in sample_user['listings'] if listing['id'] == listing_id), None)

    if listing:
        # Get the current bid amount from the form
        bid_amount = float(request.form.get('bid_amount', 0.0))

        # Ensure the bid amount is greater than the current bid
        if bid_amount > listing['min_bid']:
            # Update the minimum bid for the listing
            listing['min_bid'] = bid_amount
            bid_message = 'Bid placed successfully!'
            bid_status = 'success'
        else:
            bid_message = 'Bid must be greater than the current minimum bid.'
            bid_status = 'danger'
    else:
        bid_message = 'Listing not found.'
        bid_status = 'danger'

    # Pass bid-related messages to the template
    return render_template('product_details.html', listing=listing, bid_message=bid_message, bid_status=bid_status)

@main.route('/delete_listing/<int:listing_id>', methods=['POST'])
def delete_listing(listing_id):
    # Handle listing deletion logic here
    pass

@main.route('/checkout/<int:order_id>')
def checkout(order_id):
    # Fetch order details based on order_id
    order = next((order for order in sample_user['orders'] if order['id'] == order_id), None)
    if order:
        return render_template('checkout.html', order=order)
    else:
        # Handle order not found
        return redirect(url_for('main.shopping_cart'))

@main.route('/process_checkout/<int:order_id>', methods=['POST'])
def process_checkout(order_id):
    # Fetch order details based on order_id
    order = next((order for order in sample_user['orders'] if order['id'] == order_id), None)

    if order:
        # Process the checkout and handle the submitted form data
        full_name = request.form.get('full_name')
        address = request.form.get('address')

        # Perform the necessary actions (e.g., payment processing) and update the order status

        return render_template('checkout_success.html', order=order, full_name=full_name, address=address)
    else:
        # Handle order not found
        return redirect(url_for('main.shopping_cart'))

