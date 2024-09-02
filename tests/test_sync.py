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

    def test_get_initial_sync_returns_all_posts(self):
        setup_helper()

        response = self.client.get("/sync")

        tables = response.json()["changes"]
        posts = tables["post"]

        assert len(posts["created"]) == 2
        assert len(posts["updated"]) == 0
        assert len(posts["deleted"]) == 0

    def test_get_initial_sync_returns_all_comments(self):
        setup_helper()

        response = self.client.get("/sync")

        tables = response.json()["changes"]
        comments = tables["comment"]

        assert len(comments["created"]) == 2
        assert len(comments["updated"]) == 0
        assert len(comments["deleted"]) == 0


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
