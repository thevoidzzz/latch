"""What the model asked to do. Asking to commit is not the commit."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Proposal:
    tool: str
    draft: str
