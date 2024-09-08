from datetime import UTC, datetime
from unittest import TestCase

from fastapi.testclient import TestClient

from app.main import app
from tests.utils import clear_db


class TestGetSync(TestCase):
    client = TestClient(app)

    def test_get_sync_returns_correct_status_code(self):
        response = self.client.get("/sync")

        assert response.status_code == 200

    def test_get_sync_returns_correct_fields(self):
        response = self.client.get("/sync")

        assert "changes" in response.json()
        assert "timestamp" in response.json()

    def test_get_sync_returns_correct_tables(self):
        response = self.client.get("/sync")
        tables = response.json()["changes"]

        assert "post" in tables
        assert "comment" in tables

    def test_get_sync_returns_correct_table_changes(self):
        response = self.client.get("/sync")
        tables = response.json()["changes"]
        posts = tables["post"]

        assert "created" in posts
        assert "updated" in posts
        assert "deleted" in posts

    def test_get_initial_sync_returns_all_data(self):
        setup_helper()

        response = self.client.get("/sync")
        tables = response.json()["changes"]

        with self.subTest("Post table"):
            posts = tables["post"]
            assert len(posts["created"]) == 2
            assert len(posts["updated"]) == 0
            assert len(posts["deleted"]) == 0

        with self.subTest("Comment table"):
            comments = tables["comment"]
            assert len(comments["created"]) == 2
            assert len(comments["updated"]) == 0
            assert len(comments["deleted"]) == 0


class TestGetSyncCreated(TestCase):
    client = TestClient(app)

    def test_get_sync_with_timestamp_before_updated_at_returns_changes(self):
        last_pulled_at = datetime.now(UTC).timestamp() - 1

        setup_helper()

        response = self.client.get(f"/sync?last_pulled_at={last_pulled_at}")
        tables = response.json()["changes"]

        with self.subTest("Post table"):
            posts = tables["post"]
            assert len(posts["created"]) == 2
            assert len(posts["updated"]) == 0
            assert len(posts["deleted"]) == 0

        with self.subTest("Comment table"):
            comments = tables["comment"]
            assert len(comments["created"]) == 2
            assert len(comments["updated"]) == 0
            assert len(comments["deleted"]) == 0

    def test_get_sync_with_timestamp_after_updated_at_returns_no_changes(self):
        setup_helper()

        last_pulled_at = datetime.now(UTC).timestamp()

        response = self.client.get(f"/sync?last_pulled_at={last_pulled_at}")
        tables = response.json()["changes"]

        with self.subTest("Post table"):
            posts = tables["post"]
            assert len(posts["created"]) == 0
            assert len(posts["updated"]) == 0
            assert len(posts["deleted"]) == 0

        with self.subTest("Comment table"):
            comments = tables["comment"]
            assert len(comments["created"]) == 0
            assert len(comments["updated"]) == 0
            assert len(comments["deleted"]) == 0

    def test_get_sync_entity_has_id(self):
        setup_helper()

        response = self.client.get("/sync")
        tables = response.json()["changes"]

        with self.subTest("Post table"):
            posts = tables["post"]["created"]
            for post in posts:
                assert "id" in post

        with self.subTest("Comment table"):
            comments = tables["comment"]["created"]
            for comment in comments:
                assert "id" in comment


def setup_helper() -> None:
    client = TestClient(app)

    clear_db()

    post_with_comments = client.post(
        "/posts",
        json={"title": "Test title 1", "content": "Test content 1"},
    ).json()

    _ = client.post(
        "/posts",
        json={"title": "Test title 2", "content": "Test content 2"},
    ).json()

    _ = client.post(
        f"/posts/{post_with_comments['id']}/comments",
        json={"content": "Test comment 1"},
    )

    _ = client.post(
        f"/posts/{post_with_comments['id']}/comments",
        json={"content": "Test comment 2"},
    )
