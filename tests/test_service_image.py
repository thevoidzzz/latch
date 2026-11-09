"""The image runs the suite. Compose publishes the API and not a database."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_compose_publishes_the_api_and_not_a_database() -> None:
    compose = (ROOT / "compose.yaml").read_text(encoding="utf-8")
    dockerfile = (ROOT / "Dockerfile").read_text(encoding="utf-8")
    assert "8000:8000" in compose
    assert "5432" not in compose
    assert "5432" not in dockerfile
    assert 'ENTRYPOINT ["pytest"]' in dockerfile
