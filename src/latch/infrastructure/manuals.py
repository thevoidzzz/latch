"""Fixed manual. The passage exists only for the operator role."""

from latch.domain.hits import ManualHit

PASSAGE = "The operator logs the handoff before leaving the desk."
ROLE = "operator"


class FixedManuals:
    def search_manuals(self, question: str, role: str) -> ManualHit:
        # The question does not choose the passage. The role does.
        if role != ROLE:
            return ManualHit(None)
        return ManualHit(PASSAGE)
