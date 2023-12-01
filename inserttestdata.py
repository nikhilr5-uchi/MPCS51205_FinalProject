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

auction_items= [
{
            'id': 1,
            'user': 10,
            'title': 'Desk Lamp',
            'filenameImg': 'lamp.jpg',
            'starting_bid': 5.0,
            'expiration_date': '2023-12-31',
            'location': 'Hyde Park',
            'descriptions': 'Desk Lamp used for 5 months.',
            'buy_now_enabled': True,
            'buy_now_price': 15.0,
        },
        {
            'id': 2,
            'user': 5,
            'title': 'Study Table',
            'filenameImg': 'table.jpg',
            'starting_bid': 70.0,
            'expiration_date': '2023-12-30',
            'location': 'Hyde Park',
            'descriptions': 'Study Table used for 1 month.',
            'buy_now_enabled': False,
            'buy_now_price': 0,
        },
]

def add_to_auction(body):
    item_dict = body
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

'''
    add items to the auction website as test data
'''
if __name__ == '__main__':
    for item in auction_items:
        print(item)
        add_to_auction(item)
