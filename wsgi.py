"""Entry point of this application."""

import os
from flask import render_template
from application import create_app

app = create_app()

# Check for environment variable
if not os.environ.get("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Check for api key
if not os.environ.get("API_KEY"):
    raise RuntimeError("API key is not set")


@app.errorhandler(500)
def intrenal_server_error(error):
    """View template for 500 errors."""
    return render_template("error.html",
                           error_code=500,
                           error_message="""Sorry! It's not you, it's us.
                           Please try again."""), 500


@app.errorhandler(404)
def not_found(error):
    """View template for 404 errors."""
    return render_template("error.html",
                           error_code=404,
                           error_message="Sorry! Not found."), 404


@app.errorhandler(400)
def bad_request(error):
    """View template for 400 errors."""
    return render_template("error.html",
                           error_code=400,
                           error_message="Sorry! Bad request."), 400


if __name__ == "__main__":
    app.run()
