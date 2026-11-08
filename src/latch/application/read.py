"""Call one read port and append its name to the trace."""

from latch.application.ports import Manuals, Warehouse
from latch.domain.hits import ManualHit, WarehouseHit
from latch.domain.trace import Trace

SEARCH_MANUALS = "search_manuals"
QUERY_WAREHOUSE = "query_warehouse"


def search_manuals(question: str, role: str, manuals: Manuals, trace: Trace) -> tuple[ManualHit, Trace]:
    hit = manuals.search_manuals(question, role)
    return hit, trace.record(SEARCH_MANUALS)


def query_warehouse(question: str, warehouse: Warehouse, trace: Trace) -> tuple[WarehouseHit, Trace]:
    hit = warehouse.query_warehouse(question)
    return hit, trace.record(QUERY_WAREHOUSE)
