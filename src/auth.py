from flask import Blueprint, request, jsonify
from src import bookmarks
from src.constants.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_409_CONFLICT,
)
from werkzeug.security import generate_password_hash, check_password_hash
from src.database import Bookmark, User, db
import validators

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post("/register")
def register():
    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")
    if len(password) < 6:
        return (
            jsonify({"message": "Password must be at least 7 characters long"}),
            HTTP_400_BAD_REQUEST,
        )
    if len(username) < 3:
        return (
            jsonify({"message": "Username must be at least 4 characters long"}),
            HTTP_400_BAD_REQUEST,
        )
    if not username.isalnum() or " " in username:
        return (
            jsonify(
                {"message": "Username must be alphanumeric and cannot contain spaces"}
            ),
            HTTP_400_BAD_REQUEST,
        )
    if validators.email(email) is False:
        return (
            jsonify({"message": "Email is not valid"}),
            HTTP_400_BAD_REQUEST,
        )
    if not username or not email or not password:
        return (
            jsonify({"message": "Missing username, email or password"}),
            HTTP_400_BAD_REQUEST,
        )
    if User.query.filter_by(email=email).first():
        return (
            jsonify({"message": "Email already exists"}),
            HTTP_409_CONFLICT,
        )
    if User.query.filter_by(username=username).first():
        return (
            jsonify({"message": "Username already exists"}),
            HTTP_409_CONFLICT,
        )
    pwd_hash = generate_password_hash(password)
    user = User(username=username, email=email, password=pwd_hash)
    print(user)
    db.session.add(user)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "User created successfully",
                "user": {
                    "username": user.username,
                    "email": user.email,
                    "id": user.id,
                },
            }
        ),
        HTTP_201_CREATED,
    )


@auth.get("/me")
def index():
    return "user me"
