from flask import Flask, jsonify
import os
from src.auth import auth
from src.bookmarks import bookmarks
from src.database import db, User

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

    jwt = JWTManager(app)
    # Register a callback function that loads a user from your database whenever
    # a protected route is accessed. This should return any python object on a
    # successful lookup, or None if the lookup failed for any reason (for example
    # if the user has been deleted from the database).
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity).one_or_none()

    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
    app.run(host="  localhost", port=5000)  # port 5000 is the default port
