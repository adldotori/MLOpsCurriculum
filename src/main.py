import os
import json
from dotenv import load_dotenv

from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine

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
    user = User.objects(id=id).first()
    if not user:
        return jsonify({"error": "data not found"}), 404
    else:
        return jsonify(user.to_json()), 200


@app.route("/users", methods=["POST"])
def create_user():
    record = json.loads(request.data)
    if len(User.objects.all()) > 0:
        id = User.objects.all().order_by("-id").first()["id"] + 1
    else:
        id = 1
    user = User(id=id, name=record["name"], age=record["age"])
    try:
        user.save()
    except:
        return jsonify({"success": False}), 400
    return jsonify({"success": True}), 201


@app.route("/users/<id>", methods=["PUT"])
def update_user(id):
    record = json.loads(request.data)
    user = User.objects(id=id).first()
    if not user:
        return jsonify({"success": False}), 400
    else:
        user.update(name=record["name"])
        if "age" in record.keys():
            user.update(age=record["age"])
        user.save()
        return jsonify({"success": True}), 201


@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    user = User.objects(id=id).first()
    if not user:
        return jsonify({"success": False}), 400
    else:
        user.delete()
        return jsonify({"success": True}), 200


if __name__ == "__main__":
    app.run(debug=True)
