"""HTTP reads for the API process. The check does not construct these."""

import json
import os
import urllib.error
import urllib.request

from latch.domain.errors import ReadUnavailable
from latch.domain.hits import ManualHit, WarehouseHit


class HttpManuals:
    def __init__(self, base_url: str, timeout: float = 5.0) -> None:
        self._url = _answers_url(base_url)
        self._timeout = timeout

    def search_manuals(self, question: str, role: str) -> ManualHit:
        payload = _post(self._url, {"question": question, "role": role}, self._timeout)
        citations = payload.get("citations")
        if payload.get("refused") is True or not isinstance(citations, list) or not citations:
            return ManualHit(None)
        first = citations[0]
        excerpt = first.get("excerpt") if isinstance(first, dict) else None
        if not isinstance(excerpt, str) or excerpt == "":
            return ManualHit(None)
        return ManualHit(excerpt)


class HttpWarehouse:
    def __init__(self, base_url: str, timeout: float = 5.0) -> None:
        self._url = _answers_url(base_url)
        self._timeout = timeout

    def query_warehouse(self, question: str) -> WarehouseHit:
        payload = _post(self._url, {"question": question}, self._timeout)
        if payload.get("refused") is True:
            return WarehouseHit(None)
        value = payload.get("value")
        if value is None:
            return WarehouseHit(None)
        if not isinstance(value, str) or value == "":
            raise ReadUnavailable("the read response had no decimal")
        return WarehouseHit(value)


def from_env() -> tuple[HttpManuals | None, HttpWarehouse | None]:
    manuals = os.environ.get("LATCH_MANUALS_URL", "").strip()
    warehouse = os.environ.get("LATCH_WAREHOUSE_URL", "").strip()
    return (
        HttpManuals(manuals) if manuals else None,
        HttpWarehouse(warehouse) if warehouse else None,
    )


def _answers_url(base_url: str) -> str:
    return base_url.rstrip("/") + "/v1/answers"


def _post(url: str, body: dict[str, str], timeout: float) -> dict[str, object]:
    request = urllib.request.Request(
        url,
        data=json.dumps(body).encode(),
        headers={"content-type": "application/json", "accept": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode())
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise ReadUnavailable("the read is unavailable") from exc
    if not isinstance(payload, dict):
        raise ReadUnavailable("the read is unavailable")
    return payload
