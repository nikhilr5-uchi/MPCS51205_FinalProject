from flask_mongoengine import Document
from mongoengine.fields import StringField, EmailField

class User(Document):
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    name = StringField(max_length=1000)
