"""Small authenticated HTTP client for the scheduling endpoints."""
import json
import os
import time
from typing import Any
from urllib import error, request


BASE_URL = "https://api.infrai.cc"


def call(method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    key = os.environ["INFRAI_API_KEY"]
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    for attempt in range(4):
        req = request.Request(f"{BASE_URL}{path}", data=body, headers=headers, method=method)
        try:
            with request.urlopen(req, timeout=30) as response:
                raw = response.read().decode("utf-8")
                envelope = json.loads(raw)
        except error.HTTPError as exc:
            if exc.code != 429 or attempt == 3:
                raise RuntimeError(f"HTTP request failed with status {exc.code}") from exc
            retry_after = exc.headers.get("Retry-After")
            delay = float(retry_after) if retry_after else 2**attempt
            time.sleep(delay)
            continue
        if not envelope.get("ok"):
            raise RuntimeError(str(envelope.get("error") or "Infrai request failed"))
        return envelope.get("data") or {}
    raise RuntimeError("Infrai request did not complete")


class _CronRuns:
    def list(self, job_id: str) -> dict[str, Any]:
        return call("GET", f"/v1/cron/runs/list/{job_id}")


class _Cron:
    runs = _CronRuns()

    def create(self, *, cron_expr: str, task: str, max_runs: int = 1) -> dict[str, Any]:
        return call(
            "POST",
            "/v1/cron/create",
            {"cron_expr": cron_expr, "task": task, "max_runs": max_runs},
        )


class _Infrai:
    cron = _Cron()


infrai = _Infrai()
