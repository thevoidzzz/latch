"""A read records its tool. The wrong tool stays visible on the trace."""

from latch.application.read import query_warehouse, search_manuals
from latch.domain.trace import Trace, matches
from latch.infrastructure.manuals import PASSAGE, FixedManuals
from latch.infrastructure.warehouse import VALUE, FixedWarehouse


def test_operator_manual_returns_the_fixed_passage() -> None:
    hit, trace = search_manuals("Where is the handoff logged?", "operator", FixedManuals(), Trace())
    assert hit.passage == PASSAGE
    assert trace.tools == ("search_manuals",)
    assert matches(trace.tools, ("search_manuals",))


def test_unknown_role_is_not_a_manual_hit() -> None:
    hit, trace = search_manuals("Where is the handoff logged?", "guest", FixedManuals(), Trace())
    assert hit.passage is None
    assert trace.tools == ("search_manuals",)


def test_a_question_with_a_digit_returns_the_fixed_decimal() -> None:
    hit, trace = query_warehouse("What is desk 4 worth?", FixedWarehouse(), Trace())
    assert hit.value == VALUE
    assert trace.tools == ("query_warehouse",)


def test_a_question_without_a_number_is_refused() -> None:
    hit, _trace = query_warehouse("What is the handoff worth?", FixedWarehouse(), Trace())
    assert hit.value is None


def test_the_wrong_tool_is_visible_on_the_trace() -> None:
    _hit, trace = query_warehouse("What is desk 4 worth?", FixedWarehouse(), Trace())
    assert trace.tools == ("query_warehouse",)
    assert matches(trace.tools, ("search_manuals",)) is False
