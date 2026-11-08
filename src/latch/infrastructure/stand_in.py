"""Deterministic model. It does not open the network."""

from latch.domain.meter import Meter
from latch.domain.proposal import Proposal

CALL = Meter(1, 1.0, 1)


class StandIn:
    def meter(self) -> Meter:
        return CALL

    def propose(self, question: str, role: str) -> Proposal:
        if question.startswith("Commit"):
            return Proposal("commit_step", "Commit the step now.")
        if any(character.isdigit() for character in question):
            return Proposal("query_warehouse", "")
        return Proposal("search_manuals", "")
