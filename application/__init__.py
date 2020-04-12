"""Initialize the app."""

import os

from flask import Flask
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Globally accessible libraries
sess = Session()

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def create_app():
    """Initialize the core app."""

    # Create the app
    app = Flask(__name__, instance_relative_config=False)

    # Derive config values
    app.config.from_object("config.Config")

    # Initialiaze plugins
    sess.init_app(app)

    with app.app_context():

        # Include blueprints
        from .auth import auth_routes
        from .main import main_routes

        # Register blueprints
        app.register_blueprint(auth_routes.auth_bp)
        app.register_blueprint(main_routes.main_bp)

        return app
