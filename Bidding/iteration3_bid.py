from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client['bid_db']

bid_collection = db['bids']

example_bid = {
    'seller': 'Mark',
    'bidder': 'Jane',
    'price': '$50'
}

x = bid_collection.insert_one(example_bid)

print("test")
print(x)
print(client.list_database_names())
print(db.list_collection_names())
print(bid_collection.find())

@app.route('/bids', methods=['GET'])
def get_bids():
    bids = bid_collection.find()
    bid_list = [{'id': str(bid['_id']), 'seller': bid['seller'], 'bidder': bid['bidder'], 'price': bid['price']} for bid in bids]
    return jsonify(bid_list)

@app.route('/bids', methods=['POST'])
def create_bid():
    data = request.get_json()

    result = bid_collection.insert_one(data)

    return jsonify({'message': 'Bid created successfully', 'booking_id': str(result.inserted_id)}), 201


if __name__ == '__main__':
    app.run(debug=True)
