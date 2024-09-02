from fastapi.testclient import TestClient

from unittest import TestCase

from app.main import app


class TestGetSync(TestCase):
    client = TestClient(app)

    def test_get_sync_returns_correct_status_code(self):
        response = self.client.get("/sync")
        assert response.status_code == 200

    def test_get_sync_returns_correct_fields(self):
        response = self.client.get("/sync")

        result = response.json()[0]

        assert "created" in result
        assert "updated" in result
        assert "deleted" in result


def setup_helper() -> None:
    client = TestClient(app)

    _ = client.post(
        "/posts",
        json={"title": "Test title 1", "content": "Test content 1"},
    )

    _ = client.post(
        "/posts",
        json={"title": "Test title 2", "content": "Test content 2"},
    )

    _ = client.post(
        "/posts/1/comments",
        json={"content": "Test comment 1"},
    )

    _ = client.post(
        "/posts/2/comments",
        json={"content": "Test comment 2"},
    )
