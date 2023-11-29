import pika
import sys
from pika.exchange_type import ExchangeType
import json
from datetime import datetime
from elasticsearch import Elasticsearch

class Search:
    def __init__(self, filter, auction_items):
        self.es = ElasticSearch()