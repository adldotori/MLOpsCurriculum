from flask import jsonify
from .logger import logger


class CustomError(Exception):
    def __init__(self, status_code, error_message):
        self.status_code = status_code
        self.error_message = error_message


class UserNotFoundError(CustomError):
    def __init__(self):
        status_code = 404
        error_message = "The user is not found."
        logger.warn(error_message)
        super().__init__(status_code, error_message)


class NameIsEmptyError(CustomError):
    def __init__(self):
        status_code = 400
        error_message = '"name" parameter is empty.'
        logger.warn(error_message)
        super().__init__(status_code, error_message)


class NameAlreadyExistsError(CustomError):
    def __init__(self):
        status_code = 409
        error_message = "The user already exists."
        logger.warn(error_message)
        super().__init__(status_code, error_message)


class InvalidIdError(CustomError):
    def __init__(self):
        status_code = 400
        error_message = "Invalid user id."
        logger.warn(error_message)
        super().__init__(status_code, error_message)


class InvalidAgeError(CustomError):
    def __init__(self):
        status_code = 400
        error_message = '"age" must be an integer.'
        logger.error(error_message)
        super().__init__(status_code, error_message)


def error_handle(app):
    @app.errorhandler(CustomError)
    def handle_error(e):
        return jsonify({"message": e.error_message}), e.status_code
