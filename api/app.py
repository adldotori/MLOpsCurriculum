import os

from flask import Flask, jsonify
from flask_migrate import Migrate

from .model import db
from .routes import user_bp

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {
    "db": os.getenv("MONGO_INITDB_DATABASE"),
    "host": os.getenv("MONGO_HOST"),
    "port": int(os.getenv("MONGO_PORT")),
    "username": os.getenv("MONGO_INITDB_ROOT_USERNAME"),
    "password": os.getenv("MONGO_INITDB_ROOT_PASSWORD"),
}
db.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(user_bp, url_prefix="/users")


@app.route("/")
def health_check():
    return jsonify({"status": "OK"}), 200


if __name__ == "__main__":
    app.debug = True
    app.run()
