"""What one stand-in call costs. Not a live price."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Meter:
    cost: int
    latency_ms: float
    tokens: int
