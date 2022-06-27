from flask import Flask, jsonify
import os
from src.auth import auth
from src.bookmarks import bookmarks
from src.database import db

from flask_jwt_extended import JWTManager


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY", default="dev"),
            SQLALCHEMY_DATABASE_URI=os.environ.get(
                "SQLALCHEMY_DATABASE_URI",
                default="sqlite:///"
                + os.path.join(app.instance_path, "bookmarks.sqlite"),
            ),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY", default="JWT_SECRET_KEY"),
        )
    else:
        app.config.from_mapping(test_config)

    @app.get("/")
    def index():
        return jsonify({"message": "Hello World!"})

    db.app = app
    db.init_app(app)

    JWTManager(app)
    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
    app.run(host="  localhost", port=5000)  # port 5000 is the default port
