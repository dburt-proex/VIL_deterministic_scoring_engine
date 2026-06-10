from typing import List, Optional

from fastapi import APIRouter, Query

from app.core.models import BatchSignalInput, DashboardMetrics, HealthResponse, Route, SignalInput, VILScoreObject
from app.core.routing import DEFAULT_HALT_FLAGS, DEFAULT_THRESHOLDS
from app.core.scoring import DEFAULT_WEIGHTS
from app.service import evaluate_signal
from app.store import audit_store

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse()


@router.get("/config")
def config() -> dict:
    return {
        "weights": DEFAULT_WEIGHTS,
        "thresholds": DEFAULT_THRESHOLDS,
        "halt_flags": sorted(DEFAULT_HALT_FLAGS),
        "routes": [route.value for route in Route],
        "decision_rule": "vil_score = min(weighted_signal_score, verifiability_score)",
    }


@router.post("/score", response_model=VILScoreObject)
def score_signal(signal: SignalInput) -> VILScoreObject:
    result = evaluate_signal(signal)
    audit_store.append(result)
    return result


@router.post("/route", response_model=VILScoreObject)
def route_signal_endpoint(signal: SignalInput) -> VILScoreObject:
    result = evaluate_signal(signal)
    audit_store.append(result)
    return result


@router.post("/batch-score", response_model=List[VILScoreObject])
def batch_score(batch: BatchSignalInput) -> List[VILScoreObject]:
    results = [evaluate_signal(signal) for signal in batch.signals]
    for result in results:
        audit_store.append(result)
    return results


@router.get("/audits", response_model=List[VILScoreObject])
def list_audits(
    limit: int = Query(default=50, ge=1, le=500),
    route: Optional[Route] = None,
) -> List[VILScoreObject]:
    return audit_store.list(limit=limit, route=route)


@router.get("/metrics", response_model=DashboardMetrics)
def metrics() -> DashboardMetrics:
    return audit_store.metrics()
