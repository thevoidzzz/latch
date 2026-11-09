"""Two posts. A bad body is a problem. A no does not commit."""

import logging
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field, field_validator

from latch.application.ports import Steps
from latch.infrastructure.latch import Run, StepLog, decide, start_run

logger = logging.getLogger(__name__)


class OpenRun(BaseModel):
    model_config = ConfigDict(extra="forbid")
    question: str = Field(min_length=1)
    role: str = Field(min_length=1)

    @field_validator("question", "role")
    @classmethod
    def not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("blank")
        return value.strip()


class Approval(BaseModel):
    model_config = ConfigDict(extra="forbid")
    approved: bool


def create_app(path: str, steps: Steps | None = None) -> FastAPI:
    app = FastAPI()
    app.state.path = path
    app.state.steps = steps or StepLog()

    @app.middleware("http")
    async def attach_request_id(request: Request, call_next):  # type: ignore[no-untyped-def]
        request.state.request_id = uuid4().hex
        return await call_next(request)

    @app.exception_handler(RequestValidationError)
    async def invalid_body(request: Request, exc: RequestValidationError) -> JSONResponse:
        return _problem(request, 400, "Bad Request", _validation_detail(exc))

    @app.post("/v1/runs")
    def open_run(body: OpenRun) -> JSONResponse:
        thread_id = uuid4().hex
        run = start_run(app.state.path, thread_id, body.question, body.role, steps=app.state.steps)
        _log(run)
        return JSONResponse(_body(run))

    @app.post("/v1/runs/{thread_id}/approval")
    def approve(thread_id: str, body: Approval, request: Request) -> JSONResponse:
        try:
            run = decide(app.state.path, thread_id, body.approved, steps=app.state.steps)
        except ValueError:
            return _problem(request, 404, "Not Found", "unknown thread")
        _log(run)
        return JSONResponse(_body(run))

    return app


def _body(run: Run) -> dict[str, str]:
    return {"id": run.thread_id, "status": run.status, "draft": run.draft}


def _log(run: Run) -> None:
    logger.info(
        "thread_id=%s status=%s latency_ms=%.3f tokens=%s cost=%s",
        run.thread_id,
        run.status,
        run.latency_ms,
        run.tokens,
        run.cost,
    )


def _problem(request: Request, status: int, title: str, detail: str) -> JSONResponse:
    return JSONResponse(
        status_code=status,
        media_type="application/problem+json",
        content={
            "type": "about:blank",
            "title": title,
            "status": status,
            "detail": detail,
            "request_id": request.state.request_id,
        },
    )


def _validation_detail(exc: RequestValidationError) -> str:
    errors = exc.errors()
    if any(error.get("type") == "json_invalid" for error in errors):
        return "request body must be json"
    missing = [error.get("loc", ()) for error in errors if error.get("type") == "missing"]
    fields = {part for loc in missing for part in loc if isinstance(part, str)}
    if "question" in fields:
        return "question is required"
    if "approved" in fields:
        return "approved is required"
    if "role" in fields:
        return "role is required"
    return "request body is invalid"
