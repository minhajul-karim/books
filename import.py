"""Import table file."""

import os
import csv
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine(os.environ.get("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def main():
    """Main function."""
    with open("books.csv", newline="") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            db.execute("INSERT INTO books (isbn, title, author, year) VALUES (<:isb></:isb>n, :title, :author, :year)",
                       {"isbn": row[0], "title": row[1], "author": row[2], "year": row[3]})
            db.commit()
    print("Imported!")


if __name__ == "__main__":
    main()
