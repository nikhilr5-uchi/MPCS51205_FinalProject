from flask_mongoengine import Document
from flask_login import UserMixin
from mongoengine.fields import StringField, EmailField

class User(UserMixin, Document):
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    name = StringField(max_length=1000)
