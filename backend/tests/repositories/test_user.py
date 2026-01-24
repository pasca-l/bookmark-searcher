from uuid import UUID

import pytest

from app.repositories.user import UserRepository


@pytest.fixture
def user_repo(db):
    return UserRepository(db)


class TestUserRepository:
    def test__create_user(self, user_repo):
        user_id = user_repo.create_user(google_id="google123", email="test@example.com")

        assert isinstance(user_id, UUID)

    def test__create_multiple_users(self, user_repo):
        user_id_1 = user_repo.create_user(
            google_id="google123", email="test1@example.com"
        )
        user_id_2 = user_repo.create_user(
            google_id="google456", email="test2@example.com"
        )

        assert user_id_1 != user_id_2
