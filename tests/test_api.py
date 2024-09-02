from fastapi.testclient import TestClient

from unittest import TestCase

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

        with self.subTest("status code"):
            assert response.status_code == 200
        with self.subTest("title"):
            assert response.json()["title"] == "Test title"
        with self.subTest("content"):
            assert response.json()["content"] == "Test content"
