from typing import List

from fastapi import APIRouter

from app.core.models import BatchSignalInput, HealthResponse, SignalInput, VILScoreObject
from app.service import evaluate_signal

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse()


@router.post("/score", response_model=VILScoreObject)
def score_signal(signal: SignalInput) -> VILScoreObject:
    return evaluate_signal(signal)


@router.post("/route", response_model=VILScoreObject)
def route_signal_endpoint(signal: SignalInput) -> VILScoreObject:
    return evaluate_signal(signal)


@router.post("/batch-score", response_model=List[VILScoreObject])
def batch_score(batch: BatchSignalInput) -> List[VILScoreObject]:
    return [evaluate_signal(signal) for signal in batch.signals]
