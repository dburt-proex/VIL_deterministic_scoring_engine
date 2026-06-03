from __future__ import annotations

import hashlib
import json
from typing import Dict, List

from app.core.models import AuditRecord, CriteriaScores, Route, SignalInput


def hash_input(signal: SignalInput) -> str:
    payload = json.dumps(signal.model_dump(), sort_keys=True, default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def create_audit_record(
    signal: SignalInput,
    criteria_scores: CriteriaScores,
    weights: Dict[str, float],
    thresholds: Dict[str, float],
    weighted_signal_score: float,
    verifiability_score: float,
    vil_score: float,
    route: Route,
    reason: str,
    risk_flags: List[str],
) -> AuditRecord:
    return AuditRecord(
        signal_id=signal.signal_id,
        input_hash=hash_input(signal),
        criteria_scores=criteria_scores.as_dict(),
        weights_used=weights,
        thresholds_used=thresholds,
        weighted_signal_score=weighted_signal_score,
        verifiability_score=verifiability_score,
        vil_score=vil_score,
        route=route,
        reason=reason,
        risk_flags=risk_flags,
    )
