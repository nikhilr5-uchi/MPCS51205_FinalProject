import pika
import sys
from pika.exchange_type import ExchangeType
import json

class Item:
    def __init__(self, user, title, expiration, starting_bid, location, description, uid):
        self.user = user
        self.title = title
        self.expiration = expiration
        self.starting_bid = starting_bid
        self.location = location
        self.descriptions = description
        self.uid = uid

    # if price is high enough to add
    def IsOfferAllowed(self, priceOffer):
        return priceOffer > self.starting_bid

    def GetLocation(self):
        return self.location
    
    def SplitDescriptions(self):
        for dsc in self.descriptions:
            AddAsFilter(dsc)

    def AddAsFilter(self):
        #to handle description and parse into filterable items
        pass

    def PublishItem(self):
        connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.exchange_declare(exchange='logs', exchange_type='fanout')
        
        channel.basic_publish(exchange='logs', routing_key='', body=json.dumps(self.toJSON()))
        connection.close()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

if __name__ == '__main__':
    des = ['blue', 'small']
    item = Item('Nikhil', 'Chair', '12-12-2023', '100', 'Anywhere', des)   
    item.PublishItem()