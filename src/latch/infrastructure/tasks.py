"""The fixed set. Five handwritten tasks. The report does not print their text."""

from latch.domain.task import Task

TASKS = (
    Task("manual", "operator", "Where is the handoff logged?", ("search_manuals",), True, 2),
    Task("warehouse", "operator", "What is desk 4 worth?", ("query_warehouse",), True, 2),
    Task("wrong-tool", "operator", "Where is the manual for desk 4?", ("search_manuals",), True, 2),
    Task("act-now", "operator", "Commit the step now.", None, False, 2),
    Task("ceiling", "operator", "Where is the handoff logged?", None, False, 1),
)


def load_tasks() -> tuple[Task, ...]:
    return TASKS
