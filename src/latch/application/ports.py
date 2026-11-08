"""Read ports. The question goes in. A passage or a number comes out."""

from typing import Protocol

from latch.domain.hits import ManualHit, WarehouseHit


class Manuals(Protocol):
    def search_manuals(self, question: str, role: str) -> ManualHit:
        """Return the passage for this role, or an empty hit when the role is unknown."""


class Warehouse(Protocol):
    def query_warehouse(self, question: str) -> WarehouseHit:
        """Return one decimal, or an empty hit when the question has no number."""
