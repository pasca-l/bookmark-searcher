from typing import Any

from app.db.connection import Database, FetchType


class ChunkRepository:
    def __init__(self, db: Database):
        self.db = db

    def bulk_insert_chunks(
        self,
        bookmark_id: int,
        chunks: list[tuple[int, list[float], str]],
    ) -> int:
        if not chunks:
            return 0

        query = """
            INSERT INTO chunks (bookmark_id, chunk_index, embedding, content)
            VALUES (%s, %s, %s, %s)
        """
        params_list = [
            (bookmark_id, chunk_index, embedding, content)
            for chunk_index, embedding, content in chunks
        ]
        return self.db.execute_many(query, params_list)

    def find_similar_chunks_by_user_id(
        self,
        user_id: int,
        query_embedding: list[float],
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        query = """
            SELECT b.url, b.title, c.content,
                1 - (c.embedding <=> %s::vector) AS similarity
            FROM user_bookmarks ub
            INNER JOIN bookmarks b ON ub.bookmark_id = b.id
            INNER JOIN chunks c ON b.id = c.bookmark_id
            WHERE ub.user_id = %s
            ORDER BY c.embedding <=> %s::vector
            LIMIT %s
        """
        embedding_str = f"[{','.join(map(str, query_embedding))}]"
        result = self.db.execute_query(
            query,
            (embedding_str, user_id, embedding_str, limit),
            fetch=FetchType.ALL,
        )
        return result if isinstance(result, list) else []

    def delete_chunks_by_bookmark_id(self, bookmark_id: int) -> int:
        query = """
            DELETE FROM chunks
            WHERE bookmark_id = %s
        """
        result = self.db.execute_query(query, (bookmark_id,), fetch=FetchType.ROWCOUNT)
        return result if isinstance(result, int) else 0
