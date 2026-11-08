"""What a read returned. A miss is an empty field, not a raised error."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ManualHit:
    passage: str | None


@dataclass(frozen=True, slots=True)
class WarehouseHit:
    value: str | None
