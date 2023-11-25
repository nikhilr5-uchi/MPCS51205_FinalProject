
import sys
import os
from flask import Flask, render_template, request
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
        auction_items.append(json.loads(body))

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', auction_items=auction_items)

# @app.route('/addListing', methods=['GET','POST'])
# def addListing():
#     if request.method == "POST":
#         print(request.form["name"])
#         print(request.form["email"])
#         return

#     return render_template("index.html")

if __name__ == '__main__':
    thread = threading.Thread(target=start_consumer_queue)
    thread.start()
    app.run(debug=True)

