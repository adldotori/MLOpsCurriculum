import os

from flask import Flask
from flask_mongoengine import MongoEngine


db = MongoEngine()


class User(db.Document):
    id = db.IntField(primary_key=True)
    name = db.StringField(unique=True)
    age = db.IntField(null=True)

    def to_json(self):
        return {"id": self.id, "name": self.name, "age": self.age}
