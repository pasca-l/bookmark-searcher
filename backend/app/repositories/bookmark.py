from typing import Any, cast

from app.db.connection import Database, FetchType


class BookmarkRepository:
    def __init__(self, db: Database):
        self.db = db

    def create_bookmark(self, url: str, title: str) -> int:
        query = """
            INSERT INTO bookmarks (url, title)
            VALUES (%s, %s)
            ON CONFLICT (url) DO UPDATE SET
                title = EXCLUDED.title,
                updated_at = CURRENT_TIMESTAMP
            RETURNING id
        """
        result = self.db.execute_query(query, (url, title), fetch=FetchType.ONE)
        result = cast(dict[str, Any], result)
        return result["id"]

    def link_bookmark_to_user(self, user_id: int, bookmark_id: int) -> int:
        query = """
            INSERT INTO user_bookmarks (user_id, bookmark_id)
            VALUES (%s, %s)
            RETURNING id
        """
        result = self.db.execute_query(
            query, (user_id, bookmark_id), fetch=FetchType.ONE
        )
        result = cast(dict[str, Any], result)
        return result["id"]
