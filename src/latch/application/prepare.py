"""Read, or refuse an early commit. This step never calls commit_step."""

from dataclasses import dataclass

from latch.application.ports import Manuals, Model, Warehouse
from latch.application.read import QUERY_WAREHOUSE, SEARCH_MANUALS, query_warehouse, search_manuals
from latch.domain.ceiling import must_cut
from latch.domain.trace import Trace


@dataclass(frozen=True, slots=True)
class Prepared:
    draft: str
    trace: Trace
    cut: bool = False


def prepare(
    question: str,
    role: str,
    model: Model,
    manuals: Manuals,
    warehouse: Warehouse,
    trace: Trace | None = None,
    ceiling: int = 2,
) -> Prepared:
    current = trace or Trace()
    current, cut = _spend(current, model, ceiling)
    if cut:
        return Prepared("", current, True)
    proposal = model.propose(question, role)
    if proposal.tool == SEARCH_MANUALS or proposal.tool == QUERY_WAREHOUSE:
        current, cut = _spend(current, model, ceiling)
        if cut:
            return Prepared("", current, True)
    if proposal.tool == SEARCH_MANUALS:
        hit, current = search_manuals(question, role, manuals, current)
        draft = hit.passage if hit.passage is not None else "No passage."
        return Prepared(draft, current)
    if proposal.tool == QUERY_WAREHOUSE:
        hit, current = query_warehouse(question, warehouse, current)
        draft = hit.value if hit.value is not None else "No number."
        return Prepared(draft, current)
    return Prepared(proposal.draft, current)


def _spend(trace: Trace, model: Model, ceiling: int) -> tuple[Trace, bool]:
    meter = model.meter()
    if must_cut(trace.cost, meter.cost, ceiling):
        return trace, True
    return trace.charge(meter.cost, meter.latency_ms, meter.tokens), False
