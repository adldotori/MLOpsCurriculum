import os
import json
from dotenv import load_dotenv

from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine

from error import (
    UserNotFoundError,
    NameIsEmptyError,
    NameAlreadyExistsError,
    InvalidIdError,
    InvalidAgeError,
    error_handle,
)

load_dotenv()  # take environment variables from .env.

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {
    "db": os.getenv("MONGO_INITDB_DATABASE"),
    "host": os.getenv("MONGO_HOST"),
    "port": int(os.getenv("MONGO_PORT")),
    "username": os.getenv("MONGO_INITDB_ROOT_USERNAME"),
    "password": os.getenv("MONGO_INITDB_ROOT_PASSWORD"),
}
db = MongoEngine()
db.init_app(app)
error_handle(app)


class User(db.Document):
    id = db.IntField(primary_key=True)
    name = db.StringField(unique=True)
    age = db.IntField(null=True)

    def to_json(self):
        return {"id": self.id, "name": self.name, "age": self.age}


@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "OK"}), 200


@app.route("/users", methods=["GET"])
def get_all_users():
    user = User.objects.all()
    return jsonify([i.to_json() for i in user]), 200


@app.route("/users/<id>", methods=["GET"])
def get_user(id):
    if not isinstance(id, int) or id < 0:
        raise InvalidIdError()

    user = User.objects(id=id).first()

    if not user:
        return UserNotFoundError()
    else:
        return jsonify(user.to_json()), 200


@app.route("/users", methods=["POST"])
def create_user():
    record = json.loads(request.data)

    if "name" not in record:
        raise NameIsEmptyError()

    if "age" in record and not isinstance(record["age"], int):
        raise InvalidAgeError()

    if len(User.objects(name=record["name"])) > 0:
        raise NameAlreadyExistsError()

    if len(User.objects.all()) > 0:
        id = User.objects.all().order_by("-id").first()["id"] + 1
    else:
        id = 1

    user = User(id=id, name=record["name"], age=record["age"])
    try:
        user.save()
    except:
        return jsonify({"message": "Can't save user."}), 400
    return jsonify({"id": user.id, "name": user.name, "age": user.age}), 201


@app.route("/users/<id>", methods=["PUT"])
def update_user(id):
    if not isinstance(id, int) or id < 0:
        raise InvalidIdError()

    record = json.loads(request.data)

    if "age" in record and not isinstance(record["age"], int):
        raise InvalidAgeError()

    if len(User.objects(name=record["name"])) > 0:
        raise NameAlreadyExistsError()

    user = User.objects(id=id).first()
    if not user:
        raise UserNotFoundError()
    else:
        if "name" in record.keys():
            user.update(name=record["name"])
        if "age" in record.keys():
            user.update(age=record["age"])
        user.save()
        return jsonify({"id": user.id, "name": user.name, "age": user.age}), 201


@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    if not isinstance(id, int) or id < 0:
        raise InvalidIdError()

    user = User.objects(id=id).first()
    if not user:
        return UserNotFoundError()
    else:
        user.delete()
        return jsonify({"id": user.id, "name": user.name, "age": user.age}), 200


if __name__ == "__main__":
    app.run(debug=True)
