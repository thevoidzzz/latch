"""The same thread commits once. A request to skip the latch does not."""

from pathlib import Path

import pytest

from latch.domain.action import unapproved_commit
from latch.infrastructure.latch import StepLog, decide, start_run
from latch.infrastructure.manuals import PASSAGE
from latch.infrastructure.warehouse import VALUE


def test_a_commit_without_a_yes_counts_as_unapproved() -> None:
    assert unapproved_commit(committed=True, approved=False) == 1
    assert unapproved_commit(committed=True, approved=True) == 0
    assert unapproved_commit(committed=False, approved=False) == 0


def test_a_run_waits_and_commits_once_on_the_same_thread(tmp_path: Path) -> None:
    path = str(tmp_path / "latch.sqlite")
    steps = StepLog()
    waiting = start_run(path, "desk", "Where is the handoff logged?", "operator", steps=steps)
    assert waiting.status == "waiting"
    assert waiting.draft == PASSAGE
    assert waiting.tools == ("search_manuals",)
    assert waiting.unapproved_actions == 0
    assert steps.drafts == []

    refused = decide(path, "desk", False, steps=steps)
    assert refused.status == "refused"
    assert steps.drafts == []

    path = str(tmp_path / "other.sqlite")
    steps = StepLog()
    start_run(path, "desk", "Where is the handoff logged?", "operator", steps=steps)
    committed = decide(path, "desk", True, steps=steps)
    again = decide(path, "desk", True, steps=steps)
    assert committed.status == "committed"
    assert again.status == "committed"
    assert steps.drafts == [PASSAGE]
    assert committed.unapproved_actions == 0


def test_a_yes_on_another_thread_does_not_commit_this_one(tmp_path: Path) -> None:
    path = str(tmp_path / "latch.sqlite")
    steps = StepLog()
    start_run(path, "desk", "Where is the handoff logged?", "operator", steps=steps)
    start_run(path, "other", "What is desk 4 worth?", "operator", steps=steps)
    decide(path, "other", True, steps=steps)
    assert steps.drafts == [VALUE]
    decide(path, "desk", True, steps=steps)
    assert steps.drafts == [VALUE, PASSAGE]


def test_an_early_commit_request_does_not_run(tmp_path: Path) -> None:
    path = str(tmp_path / "latch.sqlite")
    steps = StepLog()
    waiting = start_run(path, "desk", "Commit the step now.", "operator", steps=steps)
    assert waiting.status == "waiting"
    assert waiting.tools == ()
    assert waiting.unapproved_actions == 0
    assert steps.drafts == []


def test_unknown_thread_is_rejected(tmp_path: Path) -> None:
    path = str(tmp_path / "latch.sqlite")
    with pytest.raises(ValueError, match="unknown thread"):
        decide(path, "missing", True, steps=StepLog())
