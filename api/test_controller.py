import os
from flask import Flask
import json
import mongoengine

import pytest
import mock
from unittest.mock import patch

from api.controller import Controller
from api.model import db, User
from api.error import (
    UserNotFoundError,
    NameIsEmptyError,
    NameAlreadyExistsError,
    InvalidIdError,
    InvalidAgeError,
    error_handle,
)

mongoengine.connect("test", host="mongomock://localhost")


@pytest.fixture
def app():
    return Flask(__name__)


@pytest.fixture
def controller():
    return Controller(User)


def connect_db(func):
    def wrapper(app, controller):
        with app.app_context():
            mongoengine.connect("test", host="mongomock://localhost")
            func(controller)
            mongoengine.disconnect()

    return wrapper


@connect_db
def test_create(controller):
    m = mock.MagicMock()
    m.data = json.dumps({"name": "taeho", "age": 21})

    with mock.patch("api.controller.request", m):
        ret = controller.create_user()

        assert ret[1] == 201, "status code is not correct"
        assert ret[0].json["name"] == "taeho", "name is not correct"
        assert ret[0].json["age"] == 21, "age is not correct"


@connect_db
def test_create_name_is_empty(controller):
    m = mock.MagicMock()
    m.data = json.dumps({})

    with mock.patch("api.controller.request", m):
        with pytest.raises(NameIsEmptyError):
            controller.create_user()


@connect_db
def test_create_invalid_age(controller):
    m = mock.MagicMock()
    m.data = json.dumps({"name": "", "age": "a"})

    with mock.patch("api.controller.request", m):
        with pytest.raises(InvalidAgeError):
            controller.create_user()


@connect_db
def test_create_name_already_exist(controller):
    m = mock.MagicMock()
    m.data = json.dumps({"name": "taeho", "age": 21})

    with mock.patch("api.controller.request", m):
        controller.create_user()

    with mock.patch("api.controller.request", m):
        with pytest.raises(NameAlreadyExistsError):
            controller.create_user()


@connect_db
def test_read_all(controller):
    m1 = mock.MagicMock()
    m1.data = json.dumps({"name": "test", "age": 21})
    m2 = mock.MagicMock()
    m2.data = json.dumps({"name": "test2", "age": 22})

    with mock.patch("api.controller.request", m1):
        controller.create_user()

    with mock.patch("api.controller.request", m2):
        controller.create_user()

    ret = controller.get_all_users()

    assert ret[1] == 200, "status code is not correct"
    assert len(ret[0].json) == 2, "length is not correct"
    assert ret[0].json[0]["name"] == "test", "name is not correct"
    assert ret[0].json[0]["age"] == 21, "age is not correct"
    assert ret[0].json[1]["name"] == "test2", "name is not correct"
    assert ret[0].json[1]["age"] == 22, "age is not correct"


@connect_db
def test_read(controller):
    m1 = mock.MagicMock()
    m1.data = json.dumps({"name": "test", "age": 21})
    m2 = mock.MagicMock()
    m2.data = json.dumps({"name": "test2", "age": 22})

    with mock.patch("api.controller.request", m1):
        controller.create_user()

    with mock.patch("api.controller.request", m2):
        controller.create_user()

    ret1 = controller.get_user(1)
    assert ret1[1] == 200, "status code is not correct"
    assert ret1[0].json["name"] == "test", "name is not correct"
    assert ret1[0].json["age"] == 21, "age is not correct"


@connect_db
def test_read_user_not_found(controller):
    with pytest.raises(UserNotFoundError):
        controller.get_user(1)


@connect_db
def test_update(controller):
    m1 = mock.MagicMock()
    m1.data = json.dumps({"name": "test", "age": 21})

    with mock.patch("api.controller.request", m1):
        controller.create_user()

    m_update = mock.MagicMock()
    m_update.data = json.dumps({"name": "test_update", "age": 23})

    with mock.patch("api.controller.request", m_update):
        ret = controller.update_user(1)

    assert ret[1] == 201, "status code is not correct"
    assert ret[0].json["name"] == "test_update", "name is not correct"
    assert ret[0].json["age"] == 23, "age is not correct"


@connect_db
def test_update_invalid_id(controller):
    with pytest.raises(InvalidIdError):
        controller.update_user("test")

    with pytest.raises(InvalidIdError):
        controller.update_user(-1)


@connect_db
def test_update_invalid_id(controller):
    m_create = mock.MagicMock()
    m_create.data = json.dumps({"name": "test", "age": 21})

    m_update = mock.MagicMock()
    m_update.data = json.dumps({"name": "test", "age": "string"})

    with mock.patch("api.controller.request", m_create):
        controller.create_user()

    with mock.patch("api.controller.request", m_update):
        with pytest.raises(InvalidAgeError):
            controller.update_user(1)


@connect_db
def test_update_name_already_exist(controller):
    m1 = mock.MagicMock()
    m1.data = json.dumps({"name": "test", "age": 21})
    m2 = mock.MagicMock()
    m2.data = json.dumps({"name": "test2", "age": 22})

    with mock.patch("api.controller.request", m1):
        controller.create_user()
    with mock.patch("api.controller.request", m2):
        controller.create_user()

    m_update = mock.MagicMock()
    m_update.data = json.dumps({"name": "test"})

    with mock.patch("api.controller.request", m_update):
        with pytest.raises(NameAlreadyExistsError):
            controller.update_user(2)


@connect_db
def test_update_user_not_found(controller):
    m = mock.MagicMock()
    m.data = json.dumps({"name": "test", "age": 21})

    with mock.patch("api.controller.request", m):
        with pytest.raises(UserNotFoundError):
            controller.update_user(1)


@connect_db
def test_delete(controller):
    m1 = mock.MagicMock()
    m1.data = json.dumps({"name": "test", "age": 21})

    with mock.patch("api.controller.request", m1):
        controller.create_user()

    ret = controller.delete_user(1)

    assert ret[1] == 200, "status code is not correct"
    assert ret[0].json["name"] == "test", "name is not correct"
    assert ret[0].json["age"] == 21, "age is not correct"


@connect_db
def test_delete_invalid_id(controller):
    with pytest.raises(InvalidIdError):
        controller.delete_user("test")

    with pytest.raises(InvalidIdError):
        controller.delete_user(-1)


@connect_db
def test_delete_user_not_found(controller):
    with pytest.raises(UserNotFoundError):
        controller.delete_user(1)
