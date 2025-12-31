from typing import Any

import pytest

from app.db.connection import new_database


@pytest.fixture
def db():
    database = new_database()
    yield database

    tables = ["users", "bookmarks", "user_bookmarks", "chunks"]
    query = f"TRUNCATE {', '.join(tables)} RESTART IDENTITY CASCADE"
    database.execute_query(query)


@pytest.fixture
def insert_seed_data(db):
    def _seed_func(
        users: list[dict[str, Any]] = None,
        bookmarks: list[dict[str, Any]] = None,
        user_bookmarks: list[dict[str, Any]] = None,
        chunks: list[dict[str, Any]] = None,
    ) -> None:
        for user in users or []:
            db.execute_query(
                """
                INSERT INTO users (id)
                VALUES (%s)
                """,
                (user["id"],),
            )
        for bookmark in bookmarks or []:
            db.execute_query(
                """
                INSERT INTO bookmarks (id, url, title)
                VALUES (%s, %s, %s)
                """,
                (bookmark["id"], bookmark["url"], bookmark["title"]),
            )
        for user_bookmark in user_bookmarks or []:
            db.execute_query(
                """
                INSERT INTO user_bookmarks (id, user_id, bookmark_id)
                VALUES (%s, %s, %s)
                """,
                (
                    user_bookmark["id"],
                    user_bookmark["user_id"],
                    user_bookmark["bookmark_id"],
                ),
            )
        for chunk in chunks or []:
            db.execute_query(
                """
                INSERT INTO chunks (id, bookmark_id, chunk_index, embedding, content)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    chunk["id"],
                    chunk["bookmark_id"],
                    chunk["chunk_index"],
                    chunk["embedding"],
                    chunk["content"],
                ),
            )

    return _seed_func
