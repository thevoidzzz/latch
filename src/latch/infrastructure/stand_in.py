"""Deterministic model. It does not open the network."""

from latch.domain.proposal import Proposal


class StandIn:
    def propose(self, question: str, role: str) -> Proposal:
        if question.startswith("Commit"):
            return Proposal("commit_step", "Commit the step now.")
        if any(character.isdigit() for character in question):
            return Proposal("query_warehouse", "")
        return Proposal("search_manuals", "")
