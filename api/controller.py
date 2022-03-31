import json

from flask import request, jsonify

from .model import User, db
from .error import (
    UserNotFoundError,
    NameIsEmptyError,
    NameAlreadyExistsError,
    InvalidIdError,
    InvalidAgeError,
    error_handle,
)


def get_all_users():
    user = User.objects.all()
    return jsonify([i.to_json() for i in user]), 200


def get_user(id):
    if not isinstance(id, int) or id < 0:
        raise InvalidIdError()

    user = User.objects(id=id).first()

    if not user:
        return UserNotFoundError()
    else:
        return jsonify(user.to_json()), 200


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
