"""Ports. Reads and the model stay behind these calls. The commit is separate."""

from typing import Protocol

from latch.domain.hits import ManualHit, WarehouseHit
from latch.domain.meter import Meter
from latch.domain.proposal import Proposal


class Manuals(Protocol):
    def search_manuals(self, question: str, role: str) -> ManualHit:
        """Return the passage for this role, or an empty hit when the role is unknown."""


class Warehouse(Protocol):
    def query_warehouse(self, question: str) -> WarehouseHit:
        """Return one decimal, or an empty hit when the question has no number."""


class Model(Protocol):
    def propose(self, question: str, role: str) -> Proposal:
        """Name the next tool. A commit request is not itself a commit."""

    def meter(self) -> Meter:
        """Cost, latency, and tokens of one call from this stand-in."""


class Steps(Protocol):
    def commit_step(self, draft: str) -> None:
        """Record the draft. Call this only after a yes on the same thread."""
