
import sys
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_restful import Api, Resource
from item import Item
import pika
import asyncio
import threading
import json
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)
client = MongoClient("mongodb://localhost:27017/")
db = client['items_db']
bid_collection = db['item']

auction_items = {}
uid_counter = 1

'''
task runs in the background on a different threads and consumes from the queue
refresh main page to see results from consumption
'''
def start_consumer_queue(): #consume tasks
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='logs', queue=queue_name)

    print(' [*] Waiting for logs. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        print(f" [x] {body}")
        add_to_auction(json.loads(body))

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_ordering = []
        sortType = request.form['sort']
        old_ordering = list(auction_items.values())
        print("old_ordering: ", old_ordering)
        if sortType == 'priceLowHigh':
            new_ordering = sorted(old_ordering, key=lambda x: int(x['starting_bid']), reverse=False)
        if sortType == 'priceHighLow':
            new_ordering = sorted(old_ordering, key=lambda x: int(x['starting_bid']), reverse=True)
        return render_template('index.html', auction_items=new_ordering)

    return render_template('index.html', auction_items=auction_items.values())

@app.route('/addListing', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        location = request.form['location']
        expirationDate = request.form['expirationDate']
        description = request.form['description']
        startingBid = request.form['startingBid']
        if not title:
            flash('Title is required!')
        elif not description:
            flash('Description is required!')
        else:
            global uid_counter
            new_item = Item(user="placeholder", title=title, expiration=expirationDate, starting_bid=startingBid, 
                location=location, description=description, uid=uid_counter)   
            new_item.PublishItem()
            uid_counter+=1
            return redirect(url_for('index'))

    return render_template('addListing.html')


@app.route('/removeListing', methods=('GET', 'POST'))
def remove():
    if request.method == 'POST':
        removeUID = request.form['removeUID']
        if not removeUID:
            flash('UID that is going to be removed is required!')
        else:
            print("Remove Listing with UID, ", removeUID)
            del auction_items[int(removeUID)]
            return redirect(url_for('index'))

    if (len(auction_items.keys()) == 0):
        flash('No items to be removed!')
    return render_template('removeListing.html', auction_uids = auction_items.keys())

def add_to_auction(body):
    item_dict = json.loads(body)
    auction_items[item_dict['uid']] = item_dict
    data = item_dict

    ##insert into mongo db
    result = bid_collection.insert_one(data)



if __name__ == '__main__':
    thread = threading.Thread(target=start_consumer_queue)
    thread.start()
    app.run(debug=True)

