from unittest import TestCase

from fastapi.testclient import TestClient

from app.main import app


class TestApi(TestCase):
    client = TestClient(app)

    def test_create_post(self):
        response = self.client.post(
            "/posts",
            json={"title": "Test title", "content": "Test content"},
        )

        with self.subTest("returns correct status code"):
            assert response.status_code == 200
        with self.subTest("returns id"):
            assert "id" in response.json()
        with self.subTest("returns correct title"):
            assert response.json()["title"] == "Test title"
        with self.subTest("content"):
            assert response.json()["content"] == "Test content"

    def test_get_post(self):
        response = self.client.post(
            "/posts",
            json={"title": "Test title", "content": "Test content"},
        )
        post_id = response.json()["id"]

        response = self.client.get(f"/posts/{post_id}")

        with self.subTest("returns correct status code"):
            assert response.status_code == 200
        with self.subTest("returns id"):
            assert response.json()["id"] == post_id
        with self.subTest("returns correct title"):
            assert response.json()["title"] == "Test title"
        with self.subTest("returns correct content"):
            assert response.json()["content"] == "Test content"

    def test_create_comment(self):
        response = self.client.post(
            "/posts",
            json={"title": "Test title", "content": "Test content"},
        )
        post_id = response.json()["id"]

        response = self.client.post(
            f"/posts/{post_id}/comments",
            json={"content": "Test comment"},
        )

        with self.subTest("returns correct status code"):
            assert response.status_code == 200
        with self.subTest("returns id"):
            assert "id" in response.json()
        with self.subTest("returns correct content"):
            assert response.json()["content"] == "Test comment"

    def test_get_comments(self):
        response = self.client.post(
            "/posts",
            json={"title": "Test title", "content": "Test content"},
        )
        post_id = response.json()["id"]

        _ = self.client.post(
            f"/posts/{post_id}/comments",
            json={"content": "Test comment"},
        )

        response = self.client.get(f"/posts/{post_id}/comments")

        with self.subTest("returns correct status code"):
            assert response.status_code == 200
        with self.subTest("returns correct number of comments"):
            assert len(response.json()["comments"]) == 1
        with self.subTest("returns correct comment content"):
            assert response.json()["comments"][0]["content"] == "Test comment"
