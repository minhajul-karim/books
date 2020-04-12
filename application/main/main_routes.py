"""Routes for logged in users."""

from .. import db
from flask import Blueprint, render_template, session, request, abort


# Set up a blueprint
main_bp = Blueprint("main_bp", __name__,
                    template_folder="templates")


@main_bp.route("/")
def home():
    """Home route."""
    # Check if user is logged in
    if session.get("username") is None:
        return render_template("home.html")

    return render_template("home.html",
                           name=session["username"])


@main_bp.route("/books", methods=["GET"])
def books():
    """All matching books."""

    # User input
    search_term = request.args.get("search")
    try:
        results = db.execute("""SELECT * FROM books WHERE title LIKE :search_term
                                OR author LIKE :search_term
                                OR isbn LIKE :search_term""",
                             {"search_term": '%' + search_term.lower() + '%'}).fetchall()

        return render_template("books.html",
                               search_term=search_term,
                               results=results)
    except Exception:
        abort(500)


@main_bp.route("/book/<int:book_id>", methods=["GET", "POST"])
def book(book_id):
    """View book."""

    # Retrieve data of book_id
    book = db.execute(
        "SELECT * FROM books WHERE id = :id", {"id": book_id}).fetchone()

    try:
        book = db.execute(
            "SELECT * FROM books WHERE id = :id", {"id": book_id}).fetchone()

        if book:
            return render_template("book.html",
                                   title=book["title"],
                                   author=book["author"],
                                   year=book["year"],
                                   isbn=book["isbn"])
        else:
            abort(400)
    except Exception:
        abort(500)


@main_bp.route("/test")
def test():
    """View book page."""
    if request.method == "POST":
        rating = request.form.get("rating")
        return rating
    return "try ag!"
