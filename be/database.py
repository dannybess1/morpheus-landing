"""
File to prevent circular imports when using the database.
"""

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()