import pika
import asyncio
import threading
import sys
import os
import json
from pymongo import MongoClient
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
    auction_items[item_dict['uid']] = item_dict
    data = item_dict


if __name__ == '__main__':
    start_consumer_queue()