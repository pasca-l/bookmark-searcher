import pytest

from app.repositories.bookmark import BookmarkRepository


@pytest.fixture
def bookmark_repo(db):
    return BookmarkRepository(db)


class TestBookmarkRepository:
    @pytest.mark.parametrize(
        ["seed", "url", "title", "expected"],
        [
            pytest.param(
                # no pre-existing bookmarks
                {},
                "https://example.com",
                "Example Site",
                {"id": 1},
            ),
            pytest.param(
                # with pre-existing bookmark
                {
                    "bookmarks": [
                        {
                            "id": 20,
                            "url": "https://duplicate.com",
                            "title": "First Title",
                        }
                    ]
                },
                "https://duplicate.com",
                "Updated Title",
                {"id": 20},
            ),
        ],
    )
    def test__create_bookmark(
        self, insert_seed_data, bookmark_repo, seed, url, title, expected
    ):
        insert_seed_data(**seed)
        bookmark_id = bookmark_repo.create_bookmark(url=url, title=title)

        assert isinstance(bookmark_id, int)
        assert bookmark_id > 0
        assert bookmark_id == expected["id"]

    @pytest.mark.parametrize(
        ["seed", "user_id", "bookmark_id", "expected"],
        [
            pytest.param(
                # with pre-existing user and bookmark
                {
                    "users": [{"id": 100}],
                    "bookmarks": [
                        {"id": 20, "url": "https://test.com", "title": "Test website"}
                    ],
                },
                100,
                20,
                {"id": 1},
            ),
            pytest.param(
                # error case, no pre-existing bookmark to link
                {"users": [{"id": 100}], "bookmarks": []},
                100,
                20,
                None,
                marks=pytest.mark.xfail(raises=Exception, strict=True),
            ),
            pytest.param(
                # error case, no pre-existing user to link
                {
                    "users": [],
                    "bookmarks": [
                        {"id": 20, "url": "https://test.com", "title": "Test website"}
                    ],
                },
                100,
                20,
                None,
                marks=pytest.mark.xfail(raises=Exception, strict=True),
            ),
            pytest.param(
                # error case, pre-existing link
                {
                    "users": [{"id": 100}],
                    "bookmarks": [
                        {"id": 20, "url": "https://test.com", "title": "Test website"}
                    ],
                    "user_bookmarks": [{"id": 1, "user_id": 100, "bookmark_id": 20}],
                },
                100,
                20,
                None,
                marks=pytest.mark.xfail(raises=Exception, strict=True),
            ),
        ],
    )
    def test__link_bookmark_to_user(
        self, insert_seed_data, bookmark_repo, seed, user_id, bookmark_id, expected
    ):
        insert_seed_data(**seed)
        user_bookmark_id = bookmark_repo.link_bookmark_to_user(user_id, bookmark_id)

        assert isinstance(user_bookmark_id, int)
        assert user_bookmark_id > 0
        assert user_bookmark_id == expected["id"]
