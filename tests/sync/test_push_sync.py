from unittest import TestCase

from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.db import engine
from app.main import app
from app.models import Post
from tests.utils import clear_db


class TestPushSync(TestCase):
    client = TestClient(app)

    def test_push_sync_returns_correct_status_code(self):
        response = self.client.post("/sync", json={"changes": {}})

        assert response.status_code == 200

    def test_push_sync_returns_ok(self):
        response = self.client.post("/sync", json={"changes": {}})

        assert response.json()["ok"] is True

    def test_push_sync_creates_new_post(self):
        clear_db()

        self.client.post(
            "/sync",
            json={
                "changes": {
                    "post": {
                        "created": [{"title": "Test title", "content": "Test content"}],
                        "updated": [],
                        "deleted": [],
                    }
                }
            },
        )

        with Session(engine) as session:
            posts = session.exec(select(Post)).all()

        assert len(posts) == 1

    def test_push_sync_creates_new_comment(self):
        clear_db()

        self.client.post(
            "/sync",
            json={
                "changes": {
                    "comment": {
                        "created": [
                            {"post_id": 1, "content": "Test content"},
                        ],
                        "updated": [],
                        "deleted": [],
                    }
                }
            },
        )

        with Session(engine) as session:
            comments = session.exec(select(Post)).all()

        assert len(comments) == 2
