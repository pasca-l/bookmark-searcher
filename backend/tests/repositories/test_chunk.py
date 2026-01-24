from uuid import UUID

import pytest

from app.repositories.chunk import ChunkRepository


@pytest.fixture
def chunk_repo(db):
    return ChunkRepository(db)


class TestChunkRepository:
    @pytest.mark.parametrize(
        ["seed", "bookmark_id", "chunks", "expected"],
        [
            pytest.param(
                # no pre-existing chunks
                {
                    "bookmarks": [
                        {
                            "id": "b0000000-0000-0000-0000-000000000001",
                            "url": "https://test.com",
                            "title": "Test website",
                        },
                    ]
                },
                "b0000000-0000-0000-0000-000000000001",
                [
                    (0, [0.1] * 384, "First chunk content"),
                    (1, [0.2] * 384, "Second chunk content"),
                ],
                {"count": 2},
            ),
            pytest.param(
                # insert empty chunks list
                {
                    "bookmarks": [
                        {
                            "id": "b0000000-0000-0000-0000-000000000001",
                            "url": "https://test.com",
                            "title": "Test website",
                        },
                    ]
                },
                "b0000000-0000-0000-0000-000000000001",
                [],
                {"count": 0},
            ),
        ],
    )
    def test__bulk_insert_chunks(
        self, insert_seed_data, chunk_repo, seed, bookmark_id, chunks, expected
    ):
        insert_seed_data(**seed)
        row_count = chunk_repo.bulk_insert_chunks(
            bookmark_id=bookmark_id, chunks=chunks
        )

        assert row_count == expected["count"]

    @pytest.mark.parametrize(
        ["seed", "user_id", "query_embedding", "limit", "expected"],
        [
            pytest.param(
                # pre-existing chunk data with limit
                {
                    "users": [
                        {
                            "id": "a0000000-0000-0000-0000-000000000001",
                            "google_id": "google1",
                            "email": "user1@test.com",
                        },
                        {
                            "id": "a0000000-0000-0000-0000-000000000002",
                            "google_id": "google2",
                            "email": "user2@test.com",
                        },
                    ],
                    "bookmarks": [
                        {
                            "id": "b0000000-0000-0000-0000-000000000001",
                            "url": "https://test1.com",
                            "title": "Test 1",
                        },
                        {
                            "id": "b0000000-0000-0000-0000-000000000002",
                            "url": "https://test2.com",
                            "title": "Test 2",
                        },
                    ],
                    "user_bookmarks": [
                        {
                            "id": 1,
                            "user_id": "a0000000-0000-0000-0000-000000000001",
                            "bookmark_id": "b0000000-0000-0000-0000-000000000001",
                        },
                        {
                            "id": 2,
                            "user_id": "a0000000-0000-0000-0000-000000000001",
                            "bookmark_id": "b0000000-0000-0000-0000-000000000002",
                        },
                        {
                            "id": 3,
                            "user_id": "a0000000-0000-0000-0000-000000000002",
                            "bookmark_id": "b0000000-0000-0000-0000-000000000002",
                        },
                    ],
                    "chunks": [
                        {
                            "id": 1,
                            "bookmark_id": "b0000000-0000-0000-0000-000000000001",
                            "chunk_index": 0,
                            "embedding": [
                                0.5 if i % 2 == 0 else 0.1 for i in range(384)
                            ],
                            "content": "Bookmark 10 - Chunk 0",
                        },
                        {
                            "id": 2,
                            "bookmark_id": "b0000000-0000-0000-0000-000000000001",
                            "chunk_index": 1,
                            "embedding": [
                                0.1 if i % 3 == 0 else 0.5 for i in range(384)
                            ],
                            "content": "Bookmark 10 - Chunk 1",
                        },
                        {
                            "id": 3,
                            "bookmark_id": "b0000000-0000-0000-0000-000000000002",
                            "chunk_index": 0,
                            "embedding": [0.3] * 384,
                            "content": "Bookmark 20 - Chunk 0",
                        },
                    ],
                },
                "a0000000-0000-0000-0000-000000000001",
                [0.3] * 384,
                1,
                {
                    "count": 1,
                    "chunks": [
                        {
                            "id": UUID("b0000000-0000-0000-0000-000000000002"),
                            "url": "https://test2.com",
                            "title": "Test 2",
                            "content": "Bookmark 20 - Chunk 0",
                            "similarity": 1.0,
                        },
                    ],
                },
            ),
            pytest.param(
                # user with no bookmarks
                {
                    "users": [
                        {
                            "id": "a0000000-0000-0000-0000-000000000001",
                            "google_id": "google1",
                            "email": "user1@test.com",
                        }
                    ],
                    "bookmarks": [
                        {
                            "id": "b0000000-0000-0000-0000-000000000001",
                            "url": "https://test1.com",
                            "title": "Test website",
                        }
                    ],
                    "user_bookmarks": [],
                    "chunks": [
                        {
                            "id": 1,
                            "bookmark_id": "b0000000-0000-0000-0000-000000000001",
                            "chunk_index": 0,
                            "embedding": [0.1] * 384,
                            "content": "Bookmark 10 - Chunk 0",
                        },
                        {
                            "id": 2,
                            "bookmark_id": "b0000000-0000-0000-0000-000000000001",
                            "chunk_index": 1,
                            "embedding": [0.2] * 384,
                            "content": "Bookmark 10 - Chunk 1",
                        },
                    ],
                },
                "a0000000-0000-0000-0000-000000000001",
                [0.5] * 384,
                None,
                {"count": 0, "chunks": []},
            ),
        ],
    )
    def test__find_similar_chunks_by_user_id(
        self,
        insert_seed_data,
        chunk_repo,
        seed,
        user_id,
        query_embedding,
        limit,
        expected,
    ):
        insert_seed_data(**seed)

        kwargs = {"user_id": user_id, "query_embedding": query_embedding}
        if limit is not None:
            kwargs["limit"] = limit

        results = chunk_repo.find_similar_chunks_by_user_id(**kwargs)

        assert isinstance(results, list)
        assert len(results) == expected["count"]

        for i, result in enumerate(results):
            expected_chunk = expected["chunks"][i]
            assert result == expected_chunk

    @pytest.mark.parametrize(
        ["seed", "bookmark_id", "expected"],
        [
            pytest.param(
                # pre-existing chunks to delete
                {
                    "bookmarks": [
                        {
                            "id": "b0000000-0000-0000-0000-000000000001",
                            "url": "https://test.com",
                            "title": "Test website",
                        },
                    ],
                    "chunks": [
                        {
                            "id": 1,
                            "bookmark_id": "b0000000-0000-0000-0000-000000000001",
                            "chunk_index": 0,
                            "embedding": [0.1] * 384,
                            "content": "Bookmark 10 - Chunk 0",
                        },
                        {
                            "id": 2,
                            "bookmark_id": "b0000000-0000-0000-0000-000000000001",
                            "chunk_index": 1,
                            "embedding": [0.2] * 384,
                            "content": "Bookmark 10 - Chunk 1",
                        },
                    ],
                },
                "b0000000-0000-0000-0000-000000000001",
                {"count": 2},
            ),
            pytest.param(
                # delete chunks for non-existent bookmark
                {
                    "bookmarks": [
                        {
                            "id": "b0000000-0000-0000-0000-000000000001",
                            "url": "https://test.com",
                            "title": "Test website",
                        },
                    ],
                    "chunks": [
                        {
                            "id": 1,
                            "bookmark_id": "b0000000-0000-0000-0000-000000000001",
                            "chunk_index": 0,
                            "embedding": [0.1] * 384,
                            "content": "Bookmark 10 - Chunk 0",
                        },
                        {
                            "id": 2,
                            "bookmark_id": "b0000000-0000-0000-0000-000000000001",
                            "chunk_index": 1,
                            "embedding": [0.2] * 384,
                            "content": "Bookmark 10 - Chunk 1",
                        },
                    ],
                },
                "b0000000-0000-0000-0000-999999999999",
                {"count": 0},
            ),
        ],
    )
    def test__delete_chunks_by_bookmark_id(
        self, insert_seed_data, chunk_repo, seed, bookmark_id, expected
    ):
        insert_seed_data(**seed)
        deleted_count = chunk_repo.delete_chunks_by_bookmark_id(bookmark_id=bookmark_id)

        assert deleted_count == expected["count"]
