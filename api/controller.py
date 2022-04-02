import json

from flask import request, jsonify

from .model import db
from .error import (
    UserNotFoundError,
    NameIsEmptyError,
    NameAlreadyExistsError,
    InvalidIdError,
    InvalidAgeError,
)


class Singleton(object):
    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_)
        return class_._instance


class Controller(Singleton):
    def __init__(self, user):
        Controller.user = user

    @classmethod
    def get_all_users(cls):
        user = cls.user.objects.all()
        return jsonify([i.to_json() for i in user]), 200

    @classmethod
    def get_user(cls, id):
        if not isinstance(id, int) or id < 0:
            raise InvalidIdError()

        user = cls.user.objects(id=id).first()

        if not user:
            raise UserNotFoundError()
        else:
            return jsonify(user.to_json()), 200

    @classmethod
    def create_user(cls):
        record = json.loads(request.data)

        if "name" not in record:
            raise NameIsEmptyError()

        if "age" in record and not isinstance(record["age"], int):
            raise InvalidAgeError()

        if len(cls.user.objects(name=record["name"])) > 0:
            raise NameAlreadyExistsError()

        if len(cls.user.objects.all()) > 0:
            id = User.objects.all().order_by("-id").first()["id"] + 1
        else:
            id = 1

        user = cls.user(id=id, name=record["name"], age=record["age"])
        try:
            user.save()
        except:
            return jsonify({"message": "Can't save user."}), 400
        return jsonify({"id": user.id, "name": user.name, "age": user.age}), 201

    @classmethod
    def update_user(cls, id):
        if not isinstance(id, int) or id < 0:
            raise InvalidIdError()

        record = json.loads(request.data)

        if "age" in record and not isinstance(record["age"], int):
            raise InvalidAgeError()

        if len(cls.user.objects(name=record["name"])) > 0:
            raise NameAlreadyExistsError()

        user = cls.user.objects(id=id).first()
        if not user:
            raise UserNotFoundError()
        else:
            if "name" in record.keys():
                user.update(name=record["name"])
            if "age" in record.keys():
                user.update(age=record["age"])
            user.save()
            return jsonify({"id": user.id, "name": user.name, "age": user.age}), 201

    @classmethod
    def delete_user(cls, id):
        if not isinstance(id, int) or id < 0:
            raise InvalidIdError()

        user = cls.user.objects(id=id).first()
        if not user:
            raise UserNotFoundError()
        else:
            user.delete()
            return jsonify({"id": user.id, "name": user.name, "age": user.age}), 200
