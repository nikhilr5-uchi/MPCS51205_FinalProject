import pika
import asyncio
import threading
import sys
import os
import json
import datetime

import mysql.connector

mydb = mysql.connector.connect(
host="localhost",
user="root",
password="root",
database="auction_site"
)

mycursor = mydb.cursor()

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
        return

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


def add_to_auction(body):
    item_dict = json.loads(body)
    data = item_dict
    print("DATAAA: ", data)
    insert_stmt = (
        "INSERT INTO listing (userID, product_title, imageName, min_bid, expiration_date, location, description, buy_now_enabled, buy_now_price) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )
    userId = int(data['user'])
    min_bid = float(data['starting_bid'])
    sqlValues = (userId, data['title'], data['filenameImg'], min_bid, datetime.date(2012, 3, 23) ,data['location'], data['descriptions'], True, 15)
    mycursor.execute(insert_stmt, sqlValues)
    mydb.commit()

if __name__ == '__main__':
    start_consumer_queue()