from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    JWTManager,
    current_user,
    get_jwt_identity,
    jwt_required,
)
import validators
from src import app
from src.database import Bookmark, db, User
from src.constants.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_409_CONFLICT,
)

bookmarks = Blueprint("bookmarks", __name__, url_prefix="/api/v1/bookmarks")


@bookmarks.post("/")
@jwt_required()
def add_book_mark():
    body = request.json.get("body", "")
    url = request.json.get("url", "")
    if not body:
        return (
            jsonify({"message": "No data provided"}),
            HTTP_400_BAD_REQUEST,
        )
    if not validators.url(url):
        return (
            jsonify({"message": "URL is not valid"}),
            HTTP_400_BAD_REQUEST,
        )
    if Bookmark.query.filter_by(url=url).first():
        return (
            jsonify({"message": "URL already exists"}),
            HTTP_409_CONFLICT,
        )
    print("*----------------------------------------------------")
    print(body, url, current_user.id)
    bookmark = Bookmark(body=body, url=url, user_id=current_user.id)
    db.session.add(bookmark)
    db.session.commit()
    return (
        jsonify(
            {
                "message": "Bookmark added successfully",
                "data": {
                    "id": bookmark.id,
                    "body": bookmark.body,
                    "url": bookmark.url,
                    "user_id": bookmark.user_id,
                    "created_at": bookmark.created_at,
                    "updated_at": bookmark.updated_at,
                },
            }
        ),
        HTTP_201_CREATED,
    )


@bookmarks.get("/")
@jwt_required()
def get_bookmarks():
    bookmarks = Bookmark.query.filter_by(user_id=current_user.id).all()
    return (
        jsonify(
            {
                "message": "Bookmarks retrieved successfully",
                "data": [
                    {
                        "id": bookmark.id,
                        "body": bookmark.body,
                        "url": bookmark.url,
                        "user_id": bookmark.user_id,
                        "created_at": bookmark.created_at,
                        "updated_at": bookmark.updated_at,
                    }
                    for bookmark in bookmarks
                ],
            }
        ),
        HTTP_200_OK,
    )


@bookmarks.get("/<int:id>")
@jwt_required()
def get_bookmark(id):
    bookmark = Bookmark.query.filter_by(id=id).first()
    if not bookmark:
        return (
            jsonify({"message": "Bookmark does not exist"}),
            HTTP_400_BAD_REQUEST,
        )
    return (
        jsonify(
            {
                "message": "Bookmark retrieved successfully",
                "data": {
                    "id": bookmark.id,
                    "body": bookmark.body,
                    "url": bookmark.url,
                    "user_id": bookmark.user_id,
                    "created_at": bookmark.created_at,
                    "updated_at": bookmark.updated_at,
                },
            }
        ),
        HTTP_200_OK,
    )


@bookmarks.put("/<int:id>")
@jwt_required()
def update_bookmark(id):
    bookmark = Bookmark.query.filter_by(id=id).first()
    if not bookmark:
        return (
            jsonify({"message": "Bookmark does not exist"}),
            HTTP_400_BAD_REQUEST,
        )
    body = request.json.get("body", "")
    url = request.json.get("url", "")
    if not body:
        return (
            jsonify({"message": "No data provided"}),
            HTTP_400_BAD_REQUEST,
        )
    if not validators.url(url):
        return (
            jsonify({"message": "URL is not valid"}),
            HTTP_400_BAD_REQUEST,
        )
    bookmark.body = body
    bookmark.url = url
    db.session.commit()
    return (
        jsonify(
            {
                "message": "Bookmark updated successfully",
                "data": {
                    "id": bookmark.id,
                    "body": bookmark.body,
                    "url": bookmark.url,
                    "user_id": bookmark.user_id,
                    "created_at": bookmark.created_at,
                    "updated_at": bookmark.updated_at,
                },
            }
        ),
        HTTP_200_OK,
    )


@bookmarks.delete("/<int:id>")
@jwt_required()
def delete_bookmark(id):
    bookmark = Bookmark.query.filter_by(id=id).first()
    if not bookmark:
        return (
            jsonify({"message": "Bookmark does not exist"}),
            HTTP_400_BAD_REQUEST,
        )
    db.session.delete(bookmark)
    db.session.commit()
    return (
        jsonify(
            {
                "message": "Bookmark deleted successfully",
                "data": {
                    "id": bookmark.id,
                    "body": bookmark.body,
                    "url": bookmark.url,
                    "user_id": bookmark.user_id,
                    "created_at": bookmark.created_at,
                    "updated_at": bookmark.updated_at,
                },
            }
        ),
        HTTP_200_OK,
    )
