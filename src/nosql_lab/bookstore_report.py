#!/usr/bin/env python3
"""Print a bookstore inventory report from MongoDB Atlas.

For each author in a list, print the author's name and the title and
publication year of every book that lists that author in author_ids.
"""

import logging
import os

from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Read Atlas credentials from environment variables (never hardcode them)
MONGODB_ATLAS_URL = os.getenv("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.getenv("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.getenv("MONGODB_ATLAS_PWD")

# Configure logging for status messages (connection, errors)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)


def print_author_books(author, books):
    """Print an author's name, then each linked book's title and year.

    Args:
        author: An author document from the authors collection.
        books: The books collection to search.
    """
    print(author["name"])
    # Join step: find every book whose author_ids list contains this _id
    for book in books.find({"author_ids": author["_id"]}):
        print(f"  {book['title']} ({book['published_year']})")
    print()  # blank line between authors


def main():
    """Connect to MongoDB Atlas and print the bookstore report."""
    # Stop early if any credential is missing
    if not all([MONGODB_ATLAS_URL, MONGODB_ATLAS_USER, MONGODB_ATLAS_PWD]):
        logger.error("Missing MONGODB_ATLAS_URL, MONGODB_ATLAS_USER, or MONGODB_ATLAS_PWD")
        return

    # Two authors from the loaded files, one added in Case Study 1
    author_ids = ["author_002", "author_003", "author_004"]

    client = None
    try:
        # Open the connection and confirm it works
        client = MongoClient(
            MONGODB_ATLAS_URL,
            username=MONGODB_ATLAS_USER,
            password=MONGODB_ATLAS_PWD,
        )
        client.admin.command("ping")
        logger.info("Connected to MongoDB Atlas")

        # Select the database and collections from Case Study 1
        db = client["bookstore"]
        authors = db["authors"]
        books = db["books"]

        # Count and loop over only the authors in our list
        query = {"_id": {"$in": author_ids}}
        print(f"Authors: {authors.count_documents(query)}\n")
        for author in authors.find(query):
            print_author_books(author, books)

    except PyMongoError as e:
        logger.error("MongoDB error: %s", e)
    finally:
        # Always close the client, even if something failed
        if client is not None:
            client.close()
            logger.info("Connection closed")


if __name__ == "__main__":
    main()