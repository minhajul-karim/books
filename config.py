"""Configuration."""

import os
from tempfile import mkdtemp


class Config:
    """Class to set configurations."""

    # General config
    SECRET_KEY = os.environ.get("SECRET_KEY")
    TEMPLATES_AUTO_RELOAD = True

    # Database
    DATABASE_URL = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session
    SESSION_TYPE = "filesystem"
    SESSION_FILE_DIR = mkdtemp()
    SESSION_PERMANENT = False
