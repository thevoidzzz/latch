"""The MCP surface is the two reads on the same doubles."""

import asyncio

from latch.infrastructure.manuals import PASSAGE
from latch.infrastructure.warehouse import VALUE
from latch.mcp.server import server


def test_mcp_tools_are_the_two_reads() -> None:
    tools = asyncio.run(server.list_tools())
    by_name = {tool.name: tool for tool in tools}
    assert set(by_name) == {"search_manuals", "query_warehouse"}
    assert by_name["search_manuals"].annotations.read_only_hint is True
    assert by_name["query_warehouse"].annotations.read_only_hint is True

    manual = asyncio.run(server.call_tool("search_manuals", {"question": "Where?", "role": "operator"}))
    unknown = asyncio.run(server.call_tool("search_manuals", {"question": "Where?", "role": "guest"}))
    number = asyncio.run(server.call_tool("query_warehouse", {"question": "desk 4"}))
    empty = asyncio.run(server.call_tool("query_warehouse", {"question": "desk"}))
    assert manual.structured_content["result"] == PASSAGE
    assert unknown.structured_content["result"] == "No passage."
    assert number.structured_content["result"] == VALUE
    assert empty.structured_content["result"] == "No number."
