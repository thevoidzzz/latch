"""Live reads are HTTP. The check keeps the doubles. A down peer is not an empty hit."""

import json
import socket
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

import pytest
from fastapi.testclient import TestClient

from latch.__main__ import run
from latch.api.app import create_app
from latch.domain.errors import ReadUnavailable
from latch.infrastructure.http_reads import HttpManuals, HttpWarehouse


class _Peer(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        length = int(self.headers.get("content-length", "0"))
        body = json.loads(self.rfile.read(length))
        self.server.bodies.append((self.path, body, self.headers.get("authorization")))  # type: ignore[attr-defined]
        data = json.dumps(self.server.payload).encode()  # type: ignore[attr-defined]
        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format: str, *args: object) -> None:
        return


def _serve(payload: dict[str, object]) -> tuple[ThreadingHTTPServer, str]:
    server = ThreadingHTTPServer(("127.0.0.1", 0), _Peer)
    server.payload = payload  # type: ignore[attr-defined]
    server.bodies = []  # type: ignore[attr-defined]
    Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_address[1]}"


def test_the_first_excerpt_is_the_passage_and_a_refusal_is_empty() -> None:
    server, url = _serve(
        {"refused": False, "citations": [{"excerpt": "The night desk books the close before noon."}]}
    )
    try:
        hit = HttpManuals(url).search_manuals("Where is the close?", "operator")
        assert hit.passage == "The night desk books the close before noon."
        server.payload = {"refused": True, "citations": []}  # type: ignore[attr-defined]
        assert HttpManuals(url).search_manuals("Where is the close?", "operator").passage is None
    finally:
        server.shutdown()
    path, body, authorization = server.bodies[0]
    assert path == "/v1/answers"
    assert body == {"question": "Where is the close?", "role": "operator"}
    assert authorization is None


def test_a_decimal_is_the_value_and_a_refusal_is_empty() -> None:
    server, url = _serve({"refused": False, "value": "1750.50"})
    try:
        assert HttpWarehouse(url).query_warehouse("What is desk 4 worth?").value == "1750.50"
        server.payload = {"refused": True, "value": None}  # type: ignore[attr-defined]
        assert HttpWarehouse(url).query_warehouse("What is desk 4 worth?").value is None
    finally:
        server.shutdown()
    assert server.bodies[0][1] == {"question": "What is desk 4 worth?"}


def test_a_number_that_is_not_text_is_an_error() -> None:
    server, url = _serve({"refused": False, "value": 10})
    try:
        with pytest.raises(ReadUnavailable, match="no decimal"):
            HttpWarehouse(url).query_warehouse("What is desk 4 worth?")
    finally:
        server.shutdown()


def _closed_url() -> str:
    probe = socket.socket()
    probe.bind(("127.0.0.1", 0))
    port = probe.getsockname()[1]
    probe.close()
    return f"http://127.0.0.1:{port}"


def test_a_down_read_is_503_and_hides_the_question(tmp_path: Path) -> None:
    client = TestClient(create_app(str(tmp_path / "latch.sqlite"), manuals=HttpManuals(_closed_url())))
    response = client.post("/v1/runs", json={"question": "Where is the handoff logged?", "role": "operator"})
    assert response.status_code == 503
    assert response.headers["content-type"].startswith("application/problem+json")
    assert response.json()["detail"] == "the read is unavailable"
    assert "handoff" not in response.text


def test_the_api_drafts_from_the_live_excerpt(tmp_path: Path) -> None:
    server, url = _serve(
        {"refused": False, "citations": [{"excerpt": "The operator logs the handoff before leaving the desk."}]}
    )
    try:
        client = TestClient(create_app(str(tmp_path / "latch.sqlite"), manuals=HttpManuals(url)))
        response = client.post("/v1/runs", json={"question": "Where is the handoff logged?", "role": "operator"})
    finally:
        server.shutdown()
    assert response.status_code == 200
    assert response.json()["status"] == "waiting"
    assert response.json()["draft"] == "The operator logs the handoff before leaving the desk."


def test_the_check_ignores_the_read_urls(monkeypatch: pytest.MonkeyPatch) -> None:
    closed = _closed_url()
    monkeypatch.setenv("LATCH_MANUALS_URL", closed)
    monkeypatch.setenv("LATCH_WAREHOUSE_URL", closed)
    assert run() == 0
