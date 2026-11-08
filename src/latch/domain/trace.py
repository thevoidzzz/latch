"""The tool names a run actually called. The final sentence is not part of it."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Trace:
    tools: tuple[str, ...] = ()
    cost: int = 0
    latency_ms: float = 0.0
    tokens: int = 0

    def record(self, tool: str) -> "Trace":
        return Trace(self.tools + (tool,), self.cost, self.latency_ms, self.tokens)

    def charge(self, cost: int, latency_ms: float, tokens: int) -> "Trace":
        return Trace(self.tools, self.cost + cost, self.latency_ms + latency_ms, self.tokens + tokens)


def matches(actual: tuple[str, ...], expected: tuple[str, ...]) -> bool:
    return actual == expected
