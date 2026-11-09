"""POST /v1/runs waits. A no does not commit. A bad body is a problem."""

from pathlib import Path

from fastapi.testclient import TestClient

from latch.api.app import create_app
from latch.infrastructure.latch import StepLog
from latch.infrastructure.manuals import PASSAGE


def test_a_no_does_not_commit_and_a_yes_does(tmp_path: Path, caplog) -> None:
    steps = StepLog()
    client = TestClient(create_app(str(tmp_path / "latch.sqlite"), steps))
    with caplog.at_level("INFO"):
        opened = client.post("/v1/runs", json={"question": "Where is the handoff logged?", "role": "operator"})
    assert opened.status_code == 200
    body = opened.json()
    assert body["status"] == "waiting"
    assert body["draft"] == PASSAGE
    assert "latency_ms=" in caplog.text

    refused = client.post(f"/v1/runs/{body['id']}/approval", json={"approved": False})
    assert refused.status_code == 200
    assert refused.json()["status"] == "refused"
    assert steps.drafts == []

    opened = client.post("/v1/runs", json={"question": "Where is the handoff logged?", "role": "operator"})
    committed = client.post(f"/v1/runs/{opened.json()['id']}/approval", json={"approved": True})
    assert committed.status_code == 200
    assert committed.json()["status"] == "committed"
    assert steps.drafts == [PASSAGE]


def test_a_missing_question_is_a_problem(tmp_path: Path) -> None:
    client = TestClient(create_app(str(tmp_path / "latch.sqlite")))
    response = client.post("/v1/runs", json={"role": "operator"})
    assert response.status_code == 400
    assert response.headers["content-type"].startswith("application/problem+json")
    assert response.json()["detail"] == "question is required"


def test_an_unknown_thread_is_a_problem(tmp_path: Path) -> None:
    client = TestClient(create_app(str(tmp_path / "latch.sqlite")))
    response = client.post("/v1/runs/missing/approval", json={"approved": True})
    assert response.status_code == 404
    assert response.headers["content-type"].startswith("application/problem+json")
    assert response.json()["detail"] == "unknown thread"
