"""The tool names a run actually called. The final sentence is not part of it."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Trace:
    tools: tuple[str, ...] = ()

    def record(self, tool: str) -> "Trace":
        return Trace(self.tools + (tool,))


def matches(actual: tuple[str, ...], expected: tuple[str, ...]) -> bool:
    return actual == expected
