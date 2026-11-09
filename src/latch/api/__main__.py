"""Serve the latch on port 8000. The checkpoint stays a file."""

import os

import uvicorn

from latch.api.app import create_app

PORT = 8000


def main() -> None:
    path = os.environ.get("LATCH_CHECKPOINT", "/tmp/latch.sqlite")
    uvicorn.run(create_app(path), host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    main()
