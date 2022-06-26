from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import string
import random

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        unique=True,
    )
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    bookmarks = db.relationship("Bookmark", backref="user", lazy=True)

    def __repr__(self):
        return "<User %r>" % self.username


class Bookmark(db.Model):
    __tablename__ = "bookmarks"
    id = db.Column(db.Integer, primary_key=True)  # primary key is the id
    body = db.Column(db.Text, nullable=True)
    url = db.Column(db.Text, nullable=False)
    short_url = db.Column(db.String(3), nullable=True)
    visists = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, onupdate=datetime.utcnow)

    def generate_short_char(self):
        chars = string.ascii_letters + string.digits  # + string.punctuation
        picked_chars = "".join(
            random.choices(chars, k=3)
        )  # k is the number of characters to pick from the string
        link = self.query.filter_by(
            short_url=picked_chars
        ).first()  # query.filter_by(short_url=picked_chars) is the query to check if the short_url already exists
        if link:
            return self.generate_short_char()
        return picked_chars

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.short_url = self.generate_short_char()

    def __repr__(self):
        return "<Bookmark %r>" % self.url
