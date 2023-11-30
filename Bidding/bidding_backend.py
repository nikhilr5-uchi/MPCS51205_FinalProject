from flask import Flask, request, jsonify
import mysql.connector

mydb = mysql.connector.connect(
host="localhost",
user="root",
password="root",
database="auction_site"
)

mycursor = mydb.cursor()

app = Flask(__name__)

#THIS WAS JUST A TEST

#mycursor.execute("""INSERT INTO bid (seller, bidder, price)
#VALUES ('Mark', 'Jane', 50);""")

#mydb.commit()


@app.route('/bids', methods=['GET'])
def get_bids():
    mycursor.execute("SELECT * FROM bid")
    result = mycursor.fetchall()

    bids = []
    for row in result:
        bid = {
            'id': row[0],
            'seller': row[1],
            'bidder': row[2],
            'price': row[3]
        }
        bids.append(bid)

    return jsonify(bids)

@app.route('/bids', methods=['POST'])
def create_bid():
    data = request.get_json()
    seller = data.get('seller')
    bidder = data.get('bidder')
    price = data.get('price')

    if seller and bidder and price:
        mycursor.execute(sql = f"INSERT INTO bid (seller, bidder, price) VALUES ({seller}, {bidder}, {price})")
        mydb.commit()

        return jsonify({'message': 'Bid created successfully'}), 201
    else:
        return jsonify({'error': 'Incomplete data provided'}), 400
    

@app.route('/increment_bid', methods=['PUT'])
def increment_bid():
    data = request.get_json()
    #increment_value = data.get('increment_value')  #MORE ADVANCED VERSION Assuming the client sends the increment value
    increment_value = 100

    if increment_value:
        try:
            increment_value = float(increment_value)  # Convert to float if necessary
            # Update the bid amount for the next bid by incrementing it
            mycursor.execute("SELECT MAX(price) FROM bid")
            current_max_bid = mycursor.fetchone()[0]

            if current_max_bid is None:
                return jsonify({'error': 'No bids placed yet'}), 404

            new_bid_amount = current_max_bid + increment_value

            return jsonify({'new_bid_amount': new_bid_amount}), 200
        except ValueError:
            return jsonify({'error': 'Invalid increment value provided'}), 400
    else:
        return jsonify({'error': 'Increment value not provided'}), 400

@app.route('/send_email_alert', methods=['POST'])
def send_email_alert():
    data = request.get_json()
    seller_email = data.get('seller_email')
    #item_name = data.get('item_name')  #MORE ADVANCED VERSION Assuming the item name is sent in the request
    item_name = "New bid has been placed."

    if seller_email and item_name:
        # Mock sending an email alert to the seller
        # In a real scenario, this function would send an actual email
        # Here, it just logs a message indicating the email that would be sent
        alert_message = f"Email alert would be sent to {seller_email} for item: {item_name}"
        print(alert_message)

        return jsonify({'message': 'Email alert simulated successfully'}), 200
    else:
        return jsonify({'error': 'Seller email or item name not provided'}), 400


mydb.close()

if __name__ == '__main__':
    app.run(debug=True)
