"""Serve the two reads on stdio. This does not publish a port."""

from latch.mcp.server import server


def main() -> None:
    server.run(transport="stdio")


if __name__ == "__main__":
    main()
