from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/bid_db")
db = client.your_database_name

bid_collection = db.bids

example_bid = {
    'seller': 'Mark',
    'bidder': 'Jane',
    'price': '$50'
}

bid_collection.insert_one(example_bid)

@app.route('/bids', methods=['GET'])
def get_bids():
    bookings = bid_collection.find()
    booking_list = [{'id': str(booking['_id']), 'seller': booking['seller'], 'bidder': booking['bidder'], 'price': booking['price']} for booking in bookings]
    return jsonify(booking_list)

@app.route('/bids', methods=['POST'])
def create_bid():
    data = request.get_json()

    result = bid_collection.insert_one(data)

    return jsonify({'message': 'Bid created successfully', 'booking_id': str(result.inserted_id)}), 201


if __name__ == '__main__':
    app.run(debug=True)
