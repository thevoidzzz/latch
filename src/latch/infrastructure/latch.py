"""Stop for a yes, then commit once. The wait is a sqlite file."""

import sqlite3
from dataclasses import dataclass
from typing import TypedDict

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

from latch.application.ports import Manuals, Model, Steps, Warehouse
from latch.application.prepare import prepare
from latch.domain.action import unapproved_commit
from latch.infrastructure.manuals import FixedManuals
from latch.infrastructure.stand_in import StandIn
from latch.infrastructure.warehouse import FixedWarehouse


class _State(TypedDict, total=False):
    question: str
    role: str
    draft: str
    tools: list[str]
    approved: bool
    committed: bool


@dataclass(frozen=True, slots=True)
class Run:
    thread_id: str
    status: str
    draft: str
    tools: tuple[str, ...]
    unapproved_actions: int


class StepLog:
    def __init__(self) -> None:
        self.drafts: list[str] = []

    def commit_step(self, draft: str) -> None:
        self.drafts.append(draft)


def start_run(
    path: str,
    thread_id: str,
    question: str,
    role: str,
    *,
    model: Model | None = None,
    manuals: Manuals | None = None,
    warehouse: Warehouse | None = None,
    steps: Steps | None = None,
) -> Run:
    with _open(path, model, manuals, warehouse, steps) as graph:
        config = _config(thread_id)
        graph.invoke({"question": question, "role": role, "tools": []}, config)
        return _view(graph, config)


def decide(
    path: str,
    thread_id: str,
    approved: bool,
    *,
    model: Model | None = None,
    manuals: Manuals | None = None,
    warehouse: Warehouse | None = None,
    steps: Steps | None = None,
) -> Run:
    with _open(path, model, manuals, warehouse, steps) as graph:
        config = _config(thread_id)
        snapshot = graph.get_state(config)
        if not snapshot.values and not snapshot.next:
            raise ValueError("unknown thread")
        if snapshot.next:
            graph.invoke(Command(resume=approved), config)
        return _view(graph, config)


class _Open:
    def __init__(self, saver: SqliteSaver, graph: object) -> None:
        self.saver = saver
        self.graph = graph

    def __enter__(self) -> object:
        return self.graph

    def __exit__(self, *args: object) -> None:
        self.saver.conn.close()
        return None


def _open(
    path: str,
    model: Model | None,
    manuals: Manuals | None,
    warehouse: Warehouse | None,
    steps: Steps | None,
) -> _Open:
    chosen_model = model or StandIn()
    chosen_manuals = manuals or FixedManuals()
    chosen_warehouse = warehouse or FixedWarehouse()
    chosen_steps = steps or StepLog()

    def choose(state: _State) -> dict:
        prepared = prepare(state["question"], state["role"], chosen_model, chosen_manuals, chosen_warehouse)
        return {"draft": prepared.draft, "tools": list(prepared.trace.tools)}

    def wait(state: _State) -> dict:
        approved = interrupt({"draft": state["draft"]})
        return {"approved": approved is True}

    def act(state: _State) -> dict:
        if state.get("approved") is True:
            chosen_steps.commit_step(state["draft"])
            return {"committed": True}
        return {"committed": False}

    builder = StateGraph(_State)
    builder.add_node("choose", choose)
    builder.add_node("wait", wait)
    builder.add_node("act", act)
    builder.add_edge(START, "choose")
    builder.add_edge("choose", "wait")
    builder.add_edge("wait", "act")
    builder.add_edge("act", END)
    saver = SqliteSaver(sqlite3.connect(path, check_same_thread=False))
    return _Open(saver, builder.compile(checkpointer=saver))


def _config(thread_id: str) -> dict:
    return {"configurable": {"thread_id": thread_id}}


def _view(graph: object, config: dict) -> Run:
    snapshot = graph.get_state(config)  # type: ignore[attr-defined]
    values = snapshot.values
    committed = values.get("committed") is True
    approved = values.get("approved") is True
    if snapshot.next:
        status = "waiting"
    elif committed:
        status = "committed"
    else:
        status = "refused"
    return Run(
        thread_id=config["configurable"]["thread_id"],
        status=status,
        draft=values.get("draft", ""),
        tools=tuple(values.get("tools", ())),
        unapproved_actions=unapproved_commit(committed, approved),
    )
