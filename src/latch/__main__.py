"""Print the stand-in report. Exit with an error when an unapproved action ran."""

import sys
import tempfile

from latch.application.evaluate import evaluate
from latch.domain.task import Report, format_report
from latch.infrastructure.suite import LatchRuns
from latch.infrastructure.tasks import load_tasks

ASSISTANT = "stand-in"


def render(report: Report) -> tuple[str, int]:
    text = format_report(ASSISTANT, report)
    if report.unapproved_actions == 0:
        return text, 0
    names = "".join(f"{task_id}\n" for task_id in report.unapproved_ids)
    return text + names, 1


def run() -> int:
    with tempfile.TemporaryDirectory() as directory:
        report = evaluate(load_tasks(), LatchRuns(f"{directory}/latch.sqlite"))
    text, code = render(report)
    sys.stdout.write(text)
    return code


def main() -> None:
    try:
        code = run()
    except ValueError as exc:
        raise SystemExit(str(exc)) from None
    if code:
        raise SystemExit(code)


if __name__ == "__main__":
    main()
