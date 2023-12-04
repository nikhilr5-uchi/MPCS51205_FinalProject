from flask import Blueprint, render_template, redirect, url_for, request
from . import db
from flask_login import login_required, current_user
import pymongo
from item import Item
from search import Search
from pymongo import MongoClient
import pika
import asyncio
import threading
import sys
import os
import json
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename
import mysql.connector
import hashlib

UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/images')

#Uncomment and run the block of code below if need to create the database and table
#(this is only intended to be run once)
#Alternatively just run the sql commands in a sql IDE like data grip for the same results
'''mydb = mysql.connector.connect(
host="localhost", #change as needed
user="root", #change as needed
password="root", #change as needed
)

mycursor = mydb.cursor()

# Create the database 'auction_site'
mycursor.execute("CREATE DATABASE IF NOT EXISTS auction_site")

# Switch to the 'auction_site' database
mycursor.execute("USE auction_site")

# Create the 'bid' table
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS bid (
        id INT AUTO_INCREMENT PRIMARY KEY,
        bid_amount INT
    )
""")'''


mydb = mysql.connector.connect(
host="localhost",
user="root",
password="root",
database="auction_site"
)

mycursor = mydb.cursor()

main = Blueprint('main', __name__) 

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    new_address = request.args.get('new_address')
    sqlQuery = "SELECT * FROM listing"
    print(sqlQuery)
    mycursor.execute(sqlQuery)
    all_listings = ConvertToDict(mycursor.fetchall())
    listings = []
    print(all_listings)
    print('user, ', str(createUID(current_user.email)))
    for listing in all_listings:
        print(listing['userID'])
        if listing['userID'] == createUID(current_user.email):
            listings.append(listing)
    return render_template('profile.html', name=current_user.name, email=current_user.email, user=sample_user, new_address=new_address, listings=listings)

uid_counter = 3

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
            'bid_won': False,
            'buy_now_price': 15.0
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
            'buy_now_price': 15.0,
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


@main.route('/home')
def home():
    return render_template('home.html')

@main.route('/search')
@login_required
def search():
    # Add logic for handling the search here
    return render_template('search_results.html')

@main.route('/all_listings', methods=['GET', 'POST'])
@login_required
def all_listings():
    if request.method == 'POST':
        new_ordering = []
        if 'filter' in request.form:
            sortType = request.form['sort']
            print("old_ordering: ", old_ordering)
            if sortType == 'priceLowHigh':
                new_ordering = sorted(old_ordering, key=lambda x: int(x['starting_bid']), reverse=False)
            if sortType == 'priceHighLow':
                new_ordering = sorted(old_ordering, key=lambda x: int(x['starting_bid']), reverse=True)
        else:
            searchFilter = request.form['searchItem']
    mycursor.execute("SELECT * FROM listing")
    listings = ConvertToDict(mycursor.fetchall())
    mydb.commit()
    return render_template('all_listings.html', listings=listings)

@main.route('/add_listing', methods=['GET', 'POST'])
@login_required
def add_listing():                                                             
    if request.method == 'POST':
        title = request.form['title']
        location = request.form['location']
        expirationDate = request.form['expiration_date']
        description = request.form['description']
        startingBid = request.form['starting_price']
        filenameImg=''
        if request.files['product_image'].filename != '':
                image = request.files['product_image']
                filenameImg = image.filename
                image.save(os.path.join(UPLOADS_PATH, secure_filename(image.filename)))

        global uid_counter
        new_item = Item(user=createUID(current_user.email), title=title, expiration=expirationDate, starting_bid=startingBid, 
            location=location, description=description, uid=uid_counter, filenameImg=filenameImg)   
        new_item.PublishItem()
        uid_counter+=1
        return redirect(url_for('main.all_listings')) #redirect to show all listings

    return render_template('add_listing.html')

@main.route('/shopping_cart')
@login_required
def shopping_cart():
    return render_template('shopping_cart.html', user=sample_user)

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

#THIS IS THE ORIGINAL place_bid funtion without database changes
'''@main.route('/place_bid/<int:listing_id>', methods=['POST'])
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
    return render_template('product_details.html', listing=listing, bid_message=bid_message, bid_status=bid_status)'''

@main.route('/get_listings/<int:listing_id>', methods=['GET'])
def get_listings():
    
    try:
        mycursor.execute("SELECT * FROM listing")
        result = mycursor.fetchall()
        listings = []
        for row in result:
            listing = {
                'id': row[0],
                'userID': row[1],
                'product_title': row[2],
                'image': row[3],
                'min_bid': row[4],
                'expiration_date': row[5],
                'location': row[6],
                'description': row[7],
                'buy_now_enabled': row[8],
                'buy_now_price': row[9]
            }
            listings.append(listing)
        return listings
    except Exception as e:
        print("An error occurred:", e)

#THIS IS THE NEW place_bid function where bids also get stored in databases
@main.route('/place_bid/<int:listing_id>', methods=['POST'])
def place_bid(listing_id):
    
    try:
        # Fetch the listing from the user's data
        listings = get_listings()
        listing = None
        for curr_listing in listings:
            if curr_listing['id'] == listing_id:
                listing = curr_listing
                break
        #listing = next((listing for listing in sample_user['listings'] if listing['id'] == listing_id), None)

        if listing:
            # Get the current bid amount from the form
            bid_amount = float(request.form.get('bid_amount', 0.0))

            # Ensure the bid amount is greater than the current bid
            if bid_amount > listing['min_bid']:
                # Update the minimum bid for the listing
                listing['min_bid'] = bid_amount
                sql = "INSERT INTO bid (bid_amount) VALUES (%s)"
                values = (bid_amount,)
                mycursor.execute(sql, values)
                mydb.commit()
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
    except Exception as e:
        print("An error occurred:", e)
        # Handle the error and return an error message or redirect to an error page
        error_message = 'An error occurred while placing the bid.'
        return render_template('error.html', error_message=error_message, error=e)

#Get all the bids in the database and return as a list
@main.route('/get_bids/<int:listing_id>', methods=['GET'])
def get_bids():
    
    try:
        mycursor.execute("SELECT * FROM bid")
        result = mycursor.fetchall()
        bids = []
        for row in result:
            bid = {
                'id': row[0],
                'bid_amount': row[1]
            }
            bids.append(bid)
        return bids
    except Exception as e:
        print("An error occurred:", e)

#Use largest bid in database and inrement_amount to get next bid increment
@main.route('/increment_bid/<int:listing_id>', methods=['PUT'])
def increment_bid(increment_amount):

    try:
        # Update the bid amount for the next bid by incrementing it
        mycursor.execute("SELECT MAX(bid_amount) FROM bid")
        current_max_bid = mycursor.fetchone()[0]

        if current_max_bid is None:
            return increment_amount

        new_bid_amount = current_max_bid + increment_amount

        return new_bid_amount
    
    except Exception as e:
        print("An error occurred:", e)

@main.route('/delete_listing/<int:listing_id>', methods=['POST'])
def delete_listing(listing_id):
    # Handle listing deletion logic here
    pass

@main.route('/checkout/<int:listing_id>')
def checkout(listing_id):
    # Fetch listing details based on listing_id
    listing = next((listing for listing in sample_user['listings'] if listing['id'] == listing_id), None)

    if listing:
        return render_template('checkout.html', listing=listing)
    else:
        # Handle listing not found
        return redirect(url_for('main.shopping_cart'))

@main.route('/process_checkout/<int:listing_id>', methods=['POST'])
def process_checkout(listing_id):
    # Fetch listing details based on listing_id
    listing = next((listing for listing in sample_user['listings'] if listing['id'] == listing_id), None)

    if listing:
        # Process the checkout and handle the submitted form data
        full_name = request.form.get('full_name')
        address = request.form.get('address')

        # Perform the necessary actions (e.g., payment processing) and update the order status
        listing['buy_now_enabled'] = False  # Disable buy now after purchase

        return render_template('checkout_success.html', listing=listing, full_name=full_name, address=address)
    else:
        # Handle listing not found
        return redirect(url_for('main.shopping_cart'))


def ConvertToDict(listings):
    all_items=[]
    print("listings", listings)
    for listing in listings:
        current = {
            'id': listing[0],
            'userID': listing[1],
            'product_title': listing[2],
            'image': listing[3],
            'min_bid': listing[4],
            'expiration_date': listing[5],
            'location': listing[6],
            'description': listing[7],
            'buy_now_enabled': listing[8],
            'buy_now_price' : listing[9]
        }
        all_items.append(current)
    return all_items

def createUID(email):
    res= int.from_bytes(email.encode(), 'little')
    return int(str(res)[:4])
