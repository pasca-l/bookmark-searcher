from typing import Any, cast
from uuid import UUID

from fastapi import Depends

from app.api.schemas.generated import Bookmark
from app.db.connection import Database, FetchType, new_database


class BookmarkRepository:
    def __init__(self, db: Database):
        self.db = db

    def get_bookmarks_by_user_id(self, user_id: UUID) -> list[Bookmark]:
        query = """
            SELECT b.id, b.url, b.title, b.created_at, b.updated_at
            FROM bookmarks b
            INNER JOIN user_bookmarks ub ON b.id = ub.bookmark_id
            WHERE ub.user_id = %s
            ORDER BY b.created_at DESC
        """
        result = self.db.execute_query(query, (user_id,), fetch=FetchType.ALL)
        return self._parse_bookmarks(result) if isinstance(result, list) else []

    def create_bookmark(self, url: str, title: str) -> Bookmark:
        query = """
            INSERT INTO bookmarks (url, title)
            VALUES (%s, %s)
            ON CONFLICT (url) DO UPDATE SET
                title = EXCLUDED.title,
                updated_at = CURRENT_TIMESTAMP
            RETURNING id, url, title, created_at, updated_at
        """
        result = self.db.execute_query(query, (url, title), fetch=FetchType.ONE)
        result = cast(dict[str, Any], result)
        return self._parse_bookmark(result)

    def link_bookmark_to_user(self, user_id: UUID, bookmark_id: UUID) -> int:
        query = """
            INSERT INTO user_bookmarks (user_id, bookmark_id)
            VALUES (%s, %s)
            ON CONFLICT (user_id, bookmark_id) DO NOTHING
            RETURNING id
        """
        result = self.db.execute_query(
            query, (user_id, bookmark_id), fetch=FetchType.ONE
        )
        result = cast(dict[str, Any], result)
        return result["id"]

    def _parse_bookmark(self, data: dict[str, Any]) -> Bookmark:
        return Bookmark.model_validate(
            {
                "id": data["id"],
                "url": data["url"],
                "title": data["title"],
                "created_at": data["created_at"],
                "updated_at": data["updated_at"],
            }
        )

    def _parse_bookmarks(self, data: list[dict[str, Any]]) -> list[Bookmark]:
        bookmarks = [self._parse_bookmark(d) for d in data]
        return bookmarks


def new_bookmark_repository(db: Database = Depends(new_database)) -> BookmarkRepository:
    return BookmarkRepository(db)
