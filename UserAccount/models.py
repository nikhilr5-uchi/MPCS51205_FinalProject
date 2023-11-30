from mongoengine import Document, StringField, EmailField, ObjectIdField
from flask_login import UserMixin
from bson import ObjectId

class User(UserMixin, Document):
    id = ObjectIdField(default=ObjectId, primary_key=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    name = StringField(max_length=1000)
