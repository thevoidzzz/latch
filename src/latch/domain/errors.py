"""A peer that did not answer. An empty hit is a different event."""


class ReadUnavailable(Exception):
    """The read did not return a hit. Callers must not treat this as a miss."""
