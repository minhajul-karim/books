"""DB classes."""

from . import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


class User(UserMixin, db.Model):
    """Class for users table."""

    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer,
                   primary_key=True)
    username = db.Column(db.String,
                         nullable=False)
    password = db.Column(db.String,
                         nullable=False)

    def __repr__(self):
    	"""Obj representation."""
    	return f"<User {self.username}>"