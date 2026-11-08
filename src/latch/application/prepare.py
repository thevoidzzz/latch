"""Read, or refuse an early commit. This step never calls commit_step."""

from dataclasses import dataclass

from latch.application.ports import Manuals, Model, Warehouse
from latch.application.read import QUERY_WAREHOUSE, SEARCH_MANUALS, query_warehouse, search_manuals
from latch.domain.trace import Trace


@dataclass(frozen=True, slots=True)
class Prepared:
    draft: str
    trace: Trace


def prepare(
    question: str,
    role: str,
    model: Model,
    manuals: Manuals,
    warehouse: Warehouse,
    trace: Trace | None = None,
) -> Prepared:
    current = trace or Trace()
    proposal = model.propose(question, role)
    if proposal.tool == SEARCH_MANUALS:
        hit, current = search_manuals(question, role, manuals, current)
        draft = hit.passage if hit.passage is not None else "No passage."
        return Prepared(draft, current)
    if proposal.tool == QUERY_WAREHOUSE:
        hit, current = query_warehouse(question, warehouse, current)
        draft = hit.value if hit.value is not None else "No number."
        return Prepared(draft, current)
    return Prepared(proposal.draft, current)
