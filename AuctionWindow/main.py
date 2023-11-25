
import sys
import os
from flask import Flask
from flask_restful import Api, Resource

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from ..item import Items

app = Flask(__name__)
api = Api(app)

api.add_resource(Item, '/items', endpoint = 'user')