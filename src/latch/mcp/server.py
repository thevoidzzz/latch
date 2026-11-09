"""search_manuals and query_warehouse. commit_step is not a tool here."""

from mcp.server import MCPServer
from mcp.types import ToolAnnotations

from latch.infrastructure.manuals import FixedManuals
from latch.infrastructure.warehouse import FixedWarehouse

server = MCPServer("latch_mcp")
_manuals = FixedManuals()
_warehouse = FixedWarehouse()
_READ = ToolAnnotations(
    read_only_hint=True,
    destructive_hint=False,
    idempotent_hint=True,
    open_world_hint=False,
)


@server.tool(annotations=_READ)
def search_manuals(question: str, role: str) -> str:
    """Return the passage for this role, or say there is no passage."""
    hit = _manuals.search_manuals(question, role)
    if hit.passage is None:
        return "No passage."
    return hit.passage


@server.tool(annotations=_READ)
def query_warehouse(question: str) -> str:
    """Return one decimal, or say there is no number."""
    hit = _warehouse.query_warehouse(question)
    if hit.value is None:
        return "No number."
    return hit.value
