"""Blueprint to authenticate users."""

from .. import db, lookup
from flask import Blueprint, jsonify, make_response


# Set up a blueprint
api_bp = Blueprint("api_bp", __name__)


@api_bp.route("/api/<isbn>")
def api(isbn):
    """Entertain api calls."""

    # Fetch book info from db
    try:
        book = db.execute("""SELECT * FROM books WHERE isbn = :isbn""",
                          {"isbn": isbn}).fetchone()
        if book:

            # Get rating from Goodread
            goodread_info = lookup(book["isbn"])

            return jsonify(
                {
                    "title": book["title"].title(),
                    "author": book["author"].title(),
                    "year": int(book["year"]),
                    "isbn": book["isbn"],
                    "review_count": int(goodread_info["total_rating"]),
                    "average_score": float(goodread_info["avg_rating"])
                })
        else:
            return make_response(jsonify(
                {
                    "error": {
                        "code": 404,
                        "message": "Book Not Found",
                        "errors": [{
                            "domain": "Api",
                            "message": "Book Not Found"
                        }]
                    }
                }), 404)
    except Exception:
        return 500
