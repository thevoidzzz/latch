"""Score a fixed set through a run port. This step does not open the checkpoint."""

from typing import Protocol

from latch.domain.task import Outcome, Report, Task, score, validate_tasks


class Runs(Protocol):
    def run(self, task: Task) -> Outcome:
        """Run one task and return its outcome."""


def evaluate(tasks: tuple[Task, ...], runs: Runs) -> Report:
    validate_tasks(tasks)
    return score(tasks, tuple(runs.run(task) for task in tasks))
