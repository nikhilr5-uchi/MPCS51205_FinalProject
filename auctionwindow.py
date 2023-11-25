
import sys
import os
from flask import Flask, render_template, request, redirect, url_for
from flask_restful import Api, Resource
from item import Item
import pika
import asyncio
import threading
import json

app = Flask(__name__)
api = Api(app)

auction_items = []

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

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', auction_items=auction_items)

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
            new_item = Item(title, title, expirationDate, startingBid, location, description)   
            new_item.PublishItem()
            return redirect(url_for('index'))

    return render_template('addListing.html')

def add_to_auction(body):
    item_dict = json.loads(body)
    auction_items.append(item_dict)

if __name__ == '__main__':
    thread = threading.Thread(target=start_consumer_queue)
    thread.start()
    app.run(debug=True)

