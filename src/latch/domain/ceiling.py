"""The next call is refused when it would pass the ceiling."""


def must_cut(spent: int, call_cost: int, ceiling: int) -> bool:
    if ceiling <= 0:
        raise ValueError("ceiling must be positive")
    if call_cost < 0:
        raise ValueError("call cost must not be negative")
    return spent + call_cost > ceiling
