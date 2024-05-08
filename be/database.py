import os


"""
File to prevent circular imports when using the database.
"""

# SQL db
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# Vector db
from pinecone import Pinecone, ServerlessSpec

pinecone_api_key = os.environ.get("PINECONE_API_KEY")
if not pinecone_api_key:
    raise ValueError("PINECONE_API_KEY is not set")

pc = Pinecone(api_key=pinecone_api_key)

