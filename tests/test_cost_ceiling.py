"""A call that would pass the ceiling cuts the run and does not commit."""

from pathlib import Path

import pytest

from latch.domain.ceiling import must_cut
from latch.infrastructure.latch import StepLog, decide, start_run
from latch.infrastructure.manuals import PASSAGE


def test_the_next_call_cuts_when_it_would_pass_the_ceiling() -> None:
    assert must_cut(1, 1, 1) is True
    assert must_cut(0, 1, 1) is False
    with pytest.raises(ValueError, match="ceiling must be positive"):
        must_cut(0, 1, 0)


def test_a_read_under_the_ceiling_records_cost_latency_and_tokens(tmp_path: Path) -> None:
    path = str(tmp_path / "latch.sqlite")
    steps = StepLog()
    waiting = start_run(path, "desk", "Where is the handoff logged?", "operator", steps=steps, ceiling=2)
    assert waiting.status == "waiting"
    assert waiting.draft == PASSAGE
    assert waiting.cost == 2
    assert waiting.latency_ms == 2.0
    assert waiting.tokens == 2
    assert waiting.unapproved_actions == 0
    committed = decide(path, "desk", True, steps=steps)
    assert committed.status == "committed"
    assert steps.drafts == [PASSAGE]


def test_the_ceiling_cuts_before_the_read_and_does_not_commit(tmp_path: Path) -> None:
    path = str(tmp_path / "latch.sqlite")
    steps = StepLog()
    cut = start_run(path, "desk", "Where is the handoff logged?", "operator", steps=steps, ceiling=1)
    assert cut.status == "cut"
    assert cut.tools == ()
    assert cut.cost == 1
    assert cut.latency_ms == 1.0
    assert cut.tokens == 1
    assert cut.unapproved_actions == 0
    assert steps.drafts == []
    still = decide(path, "desk", True, steps=steps)
    assert still.status == "cut"
    assert steps.drafts == []
