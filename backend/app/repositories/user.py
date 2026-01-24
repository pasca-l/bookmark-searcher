from dataclasses import dataclass
from typing import Any, cast
from uuid import UUID

from fastapi import Depends

from app.db.connection import Database, FetchType, new_database


@dataclass
class User:
    id: UUID
    google_id: str
    email: str
    created_at: str
    updated_at: str


class UserRepository:
    def __init__(self, db: Database):
        self.db = db

    def create_user(self, google_id: str, email: str) -> UUID:
        query = """
            INSERT INTO users (google_id, email)
            VALUES (%s, %s)
            RETURNING id
        """
        result = self.db.execute_query(query, (google_id, email), fetch=FetchType.ONE)
        result = cast(dict[str, Any], result)
        return result["id"]

    def get_user(self, google_id: str) -> User | None:
        query = """
            SELECT id, google_id, email, created_at, updated_at
            FROM users
            WHERE google_id = %s
        """
        result = self.db.execute_query(query, (google_id,), fetch=FetchType.ONE)
        if result is None:
            return None

        result = cast(dict[str, Any], result)
        return self._parse_user(result)

    def _parse_user(self, data: dict[str, Any]) -> User:
        return User(
            id=data["id"],
            google_id=data["google_id"],
            email=data["email"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
        )


def new_user_repository(db: Database = Depends(new_database)) -> UserRepository:
    return UserRepository(db)
