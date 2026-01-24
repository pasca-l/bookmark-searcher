from enum import Enum, auto
from typing import Any
from uuid import UUID

from fastapi import Depends

from app.db.connection import Database, new_database
from app.repositories.chunk import ChunkRepository
from app.services.embedding_model import EmbeddingModel, new_embedding_model


class ChunkType(Enum):
    CHARACTER = auto()
    TOKENIZER = auto()


class EmbeddingService:
    def __init__(
        self,
        db: Database,
        model: EmbeddingModel,
        chunk_type: ChunkType = ChunkType.TOKENIZER,
    ):
        self.chunk_repo = ChunkRepository(db)
        self.model = model
        self.chunk_type = chunk_type

    def store_bookmark_embedding(self, bookmark_id: UUID, content: str) -> int:
        match self.chunk_type:
            case ChunkType.CHARACTER:
                chunks = self._chunk_text_by_character(content)
            case ChunkType.TOKENIZER:
                chunks = self._chunk_text_by_tokenizer(content)
            case _:
                chunks = None

        if not chunks:
            return 0

        # generate embeddings for chunks
        embeddings = self.model.encode(chunks)

        data = [
            (chunk_index, embedding, chunk)
            for chunk_index, (embedding, chunk) in enumerate(zip(embeddings, chunks))
        ]
        return self.chunk_repo.bulk_insert_chunks(bookmark_id, data)

    def delete_bookmark_embedding(self, bookmark_id: UUID) -> int:
        return self.chunk_repo.delete_chunks_by_bookmark_id(bookmark_id)

    def search_bookmark_embedding(
        self, user_id: UUID, query: str, limit: int = 10
    ) -> list[dict[str, Any]]:
        # generate embedding for query
        query_embedding = self.model.encode([query])[0]

        return self.chunk_repo.find_similar_chunks_by_user_id(
            user_id=user_id, query_embedding=query_embedding, limit=limit
        )

    def _chunk_text_by_character(self, text: str, chunk_size: int = 500) -> list[str]:
        if not text.strip():
            return []

        chunks = []

        # if text has average space separated length, use word-based chunking
        word_threshold = 20
        words = text.split()
        if len(words) > 1 and len(text) / len(words) < word_threshold:
            for i in range(0, len(words), chunk_size):
                chunk = " ".join(words[i : i + chunk_size])
                chunks.append(chunk)
            return chunks

        # if text has no spaces, use character-based chunking
        adjust_multiplier = 5
        for i in range(0, len(text), chunk_size * adjust_multiplier):
            chunk = text[i : i + chunk_size * adjust_multiplier]
            chunks.append(chunk)

        return chunks

    def _chunk_text_by_tokenizer(self, text: str, chunk_size: int = 256) -> list[str]:
        if not text.strip():
            return []

        # tokenize whole text
        tokens = self.model.tokenizer.encode(text, add_special_tokens=False)
        chunks = []
        for i in range(0, len(tokens), chunk_size):
            chunk_tokens = tokens[i : i + chunk_size]
            # decode tokens back to text
            chunk = self.model.tokenizer.decode(chunk_tokens)
            chunks.append(chunk)

        return chunks


def new_embedding_service(
    db: Database = Depends(new_database),
    model: EmbeddingModel = Depends(new_embedding_model),
) -> EmbeddingService:
    return EmbeddingService(db, model)
