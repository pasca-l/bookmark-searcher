from dataclasses import dataclass
from typing import Any, cast
from uuid import UUID

from fastapi import Depends

from app.db.connection import Database, FetchType, new_database


@dataclass
class User:
    id: UUID
    username: str
    password_hash: str
    created_at: str
    updated_at: str


class UserRepository:
    def __init__(self, db: Database):
        self.db = db

    def create_user(self, username: str, password: str) -> UUID:
        query = """
            INSERT INTO users (username, user_password)
            VALUES (%s, %s)
            RETURNING id
        """
        result = self.db.execute_query(
            query, (username, password), fetch=FetchType.ONE
        )
        result = cast(dict[str, Any], result)
        return result["id"]

    def get_user_by_username(self, username: str) -> User | None:
        query = """
            SELECT id, username, user_password, created_at, updated_at
            FROM users
            WHERE username = %s
        """
        result = self.db.execute_query(query, (username,), fetch=FetchType.ONE)
        if result is None:
            return None

        result = cast(dict[str, Any], result)
        return self._parse_user(result)

    def _parse_user(self, data: dict[str, Any]) -> User:
        return User(
            id=data["id"],
            username=data["username"],
            password_hash=data["user_password"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
        )


def new_user_repository(db: Database = Depends(new_database)) -> UserRepository:
    return UserRepository(db)
