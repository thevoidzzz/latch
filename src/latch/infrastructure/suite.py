"""Run the fixed set on the stand-in. A yes is sent only when the task asks for one."""

from latch.application.ports import Steps
from latch.domain.task import Outcome, Task
from latch.infrastructure.latch import StepLog, decide, start_run


class LatchRuns:
    def __init__(self, path: str, steps: Steps | None = None) -> None:
        self.path = path
        self.steps = steps or StepLog()

    def run(self, task: Task) -> Outcome:
        current = start_run(
            self.path,
            task.id,
            task.text,
            task.role,
            steps=self.steps,
            ceiling=task.ceiling,
        )
        if task.approve and current.status == "waiting":
            current = decide(self.path, task.id, True, steps=self.steps)
        return Outcome(task.id, current.tools, current.unapproved_actions, current.status, current.cost)
