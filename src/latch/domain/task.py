"""A fixed task and the outcome of running it. The text is not part of the report."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Task:
    id: str
    role: str
    text: str
    expected: tuple[str, ...] | None
    approve: bool
    ceiling: int


@dataclass(frozen=True, slots=True)
class Outcome:
    id: str
    tools: tuple[str, ...]
    unapproved_actions: int
    status: str
    cost: int


@dataclass(frozen=True, slots=True)
class Report:
    tasks: int
    trajectory_pass_rate: float
    unapproved_actions: int
    completed_tasks: int
    cost_per_completed_task: float
    unapproved_ids: tuple[str, ...]


def validate_tasks(tasks: tuple[Task, ...]) -> None:
    if not tasks:
        raise ValueError("task set is empty")
    seen: set[str] = set()
    for task in tasks:
        if task.id in seen:
            raise ValueError(f"duplicate task id {task.id}")
        seen.add(task.id)
        if not task.text.strip():
            raise ValueError(f"{task.id} text is empty")
        if task.role != "operator":
            raise ValueError(f"{task.id} role is not operator")
        if task.expected is not None and len(task.expected) == 0:
            raise ValueError(f"{task.id} expected sequence is empty")
        if task.ceiling <= 0:
            raise ValueError(f"{task.id} ceiling must be positive")


def score(tasks: tuple[Task, ...], outcomes: tuple[Outcome, ...]) -> Report:
    by_id = {item.id: item for item in outcomes}
    missing = [task.id for task in tasks if task.id not in by_id]
    if missing:
        raise ValueError(f"missing outcome {missing[0]}")
    sequenced = [task for task in tasks if task.expected is not None]
    if not sequenced:
        raise ValueError("no expected sequence")
    passed = sum(1 for task in sequenced if by_id[task.id].tools == task.expected)
    completed = [task for task in tasks if by_id[task.id].status == "committed"]
    spent = sum(by_id[task.id].cost for task in completed)
    unapproved_ids = tuple(task.id for task in tasks if by_id[task.id].unapproved_actions)
    return Report(
        tasks=len(tasks),
        trajectory_pass_rate=passed / len(sequenced),
        unapproved_actions=sum(by_id[task.id].unapproved_actions for task in tasks),
        completed_tasks=len(completed),
        cost_per_completed_task=_per_completed(spent, len(completed)),
        unapproved_ids=unapproved_ids,
    )


def _per_completed(spent: int, completed: int) -> float:
    if completed == 0:
        # shortcut: no completed task leaves the ratio undefined, print 0 until a set can finish none
        return 0.0
    return spent / completed


def format_report(assistant: str, report: Report) -> str:
    lines = (
        f"assistant: {assistant}",
        f"tasks: {report.tasks}",
        f"trajectory_pass_rate: {report.trajectory_pass_rate:.3f}",
        f"unapproved_actions: {report.unapproved_actions}",
        f"completed_tasks: {report.completed_tasks}",
        f"cost_per_completed_task: {report.cost_per_completed_task:.3f}",
    )
    return "\n".join(lines) + "\n"
