"""Routes for logged in users."""

from .. import db, lookup
from datetime import datetime
from flask import (Blueprint, render_template,
                   session, request, abort, flash, redirect, url_for)


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
                               term=search_term,
                               search_term=search_term,
                               results=results)
    except Exception:
        abort(500)


@main_bp.route("/book/<int:book_id>")
@main_bp.route("/book", defaults={"book_id": None}, methods=["POST"])
def book(book_id):
    """View book."""

    # When user submits a review
    if request.method == "POST":
        rating = request.form.get("rating")
        comment = request.form.get("comment")
        if rating:
            # Submit review
            try:
                # Insert reveiw into db
                db.execute("""INSERT INTO reviews (user_id, book_id, rating, comment, posted_on)
                                VALUES (:user_id, :book_id, :rating, :comment, :posted_on)""",
                           {"user_id": session["user_id"],
                            "book_id": session["book_id"],
                            "rating": rating,
                            "comment": comment,
                            "posted_on": datetime.utcnow().date()})
                db.commit()
                return redirect(url_for('.book', book_id=session["book_id"]))

            except Exception:
                abort(500)
        else:
            flash("Please give a rating to submit review.")
            return redirect(url_for('.book', book_id=session["book_id"]))

    else:
        # When user visits a book page
        try:

            # Get all reviews for a book
            reviews = db.execute("""SELECT username, rating, comment, posted_on
                                FROM reviews
                                INNER JOIN users ON users.id = reviews.user_id
                                WHERE book_id = :book_id
                                ORDER BY posted_on DESC""",
                                 {"book_id": book_id}).fetchall()

            # Check logged in user's past reviews
            past_review = False
            if "user_id" in session:
                # Save book_id to seeion
                session["book_id"] = book_id
                for review in reviews:
                    if review["username"] == session["username"]:
                        past_review = True

            print(past_review)
            # Get book information
            book = db.execute("""SELECT * FROM books WHERE id = :id""",
                              {"id": book_id}).fetchone()

            if book:

                # Get rating from Goodread
                # goodread_info = lookup(book["isbn"])

                return render_template("book.html",
                                       term=book["title"],
                                       search_term=book["title"],
                                       title=book["title"],
                                       author=book["author"],
                                       year=book["year"],
                                       isbn=book["isbn"],
                                       past_review=past_review,
                                       reviews=reviews)
            else:
                abort(400)

        except Exception:
            abort(500)


@main_bp.route("/test")
def test():
    rating = request.args.get("rating")
    print(rating)
    return rating
