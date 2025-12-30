from typing import Any, cast

from app.db.connection import Database, FetchType


class UserRepository:
    def __init__(self, db: Database):
        self.db = db

    def create_user(self) -> int:
        query = """
            INSERT INTO users DEFAULT VALUES
            RETURNING id
        """
        result = self.db.execute_query(query, fetch=FetchType.ONE)
        result = cast(dict[str, Any], result)
        return result["id"]
