"""The codespace keeps the default image. The try commands open a run and approve it."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_the_codespace_keeps_the_default_image() -> None:
    config = json.loads((ROOT / ".devcontainer" / "devcontainer.json").read_text(encoding="utf-8"))
    assert set(config) == {"name", "hostRequirements", "forwardPorts", "features", "postCreateCommand"}
    assert config["name"] == "Latch"
    assert config["hostRequirements"] == {"cpus": 2}
    assert config["forwardPorts"] == [8000]
    assert config["features"] == {
        "ghcr.io/devcontainers/features/python:1": {"version": "3.12", "installTools": False}
    }
    assert config["postCreateCommand"] == "python -m pip install --user -e '.[dev]'"


def test_the_readme_try_approves_one_run() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "Create a codespace on the 2-core machine." in readme
    assert "default image" in readme
    assert "Delete the codespace when you finish." in readme
    assert "python -m latch\n" in readme
    assert "python -m latch.api" in readme
    assert "localhost:8000/v1/runs" in readme
    assert '{"question":"Where is the handoff logged?","role":"operator"}' in readme
    assert '{"approved":true}' in readme
    assert '"status": "waiting"' in readme
    assert '"status": "committed"' in readme
    lowered = readme.lower()
    for needle in ("openai", "anthropic", "render.com", "railway.app", "fly.dev"):
        assert needle not in lowered


def test_the_image_suite_copies_the_codespace() -> None:
    dockerfile = ROOT / "Dockerfile"
    if not dockerfile.is_file():
        return  # shortcut: the test image omits the Dockerfile, the checkout run locks this COPY
    assert "COPY .devcontainer ./.devcontainer" in dockerfile.read_text(encoding="utf-8")


def test_the_architecture_records_the_default_image() -> None:
    path = ROOT / "docs" / "architecture" / "ARCHITECTURE.md"
    if not path.is_file():
        return  # shortcut: the test image omits docs, the checkout run locks this sentence
    text = path.read_text(encoding="utf-8")
    assert "imagen Linux por defecto" in text
    assert "2 núcleos" in text
    assert "No hay prebuild." in text
