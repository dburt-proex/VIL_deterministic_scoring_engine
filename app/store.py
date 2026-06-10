from __future__ import annotations

import json
import os
from pathlib import Path
from threading import Lock
from typing import List, Optional

from app.core.models import DashboardMetrics, Route, VILScoreObject


class AuditLogStore:
    """Durable JSONL audit store for the commercial dashboard MVP.

    This keeps VIL deployable without a database while preserving replayable score
    decisions. Replace with Postgres or SQLite when multi-user tenancy is required.
    """

    def __init__(self, path: str | None = None) -> None:
        self.path = Path(path or os.getenv("VIL_AUDIT_LOG", "data/audit_log.jsonl"))
        self._lock = Lock()
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, score_object: VILScoreObject) -> None:
        payload = score_object.model_dump(mode="json")
        with self._lock:
            with self.path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(payload, sort_keys=True) + "\n")

    def list(self, limit: int = 50, route: Optional[Route] = None) -> List[VILScoreObject]:
        if not self.path.exists():
            return []

        entries: List[VILScoreObject] = []
        with self._lock:
            lines = self.path.read_text(encoding="utf-8").splitlines()

        for line in reversed(lines):
            if not line.strip():
                continue
            try:
                item = VILScoreObject.model_validate(json.loads(line))
            except (json.JSONDecodeError, ValueError):
                continue
            if route and item.route != route:
                continue
            entries.append(item)
            if len(entries) >= limit:
                break
        return entries

    def metrics(self) -> DashboardMetrics:
        entries = self.list(limit=10000)
        total = len(entries)
        route_counts = {route.value: 0 for route in Route}
        for entry in entries:
            route_counts[entry.route.value] = route_counts.get(entry.route.value, 0) + 1

        average = round(sum(entry.vil_score for entry in entries) / total, 2) if total else 0.0
        pass_rate = round((route_counts.get(Route.PASS.value, 0) / total) * 100, 1) if total else 0.0
        review_load = route_counts.get(Route.REVIEW.value, 0) + route_counts.get(Route.CLARIFY.value, 0)
        latest = entries[0].audit.created_at if entries else None
        return DashboardMetrics(
            total_signals=total,
            route_counts=route_counts,
            average_vil_score=average,
            pass_rate=pass_rate,
            review_load=review_load,
            halt_count=route_counts.get(Route.HALT.value, 0),
            latest_audit_at=latest,
        )


audit_store = AuditLogStore()
