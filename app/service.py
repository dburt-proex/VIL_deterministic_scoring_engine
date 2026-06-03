from app.core.audit import create_audit_record
from app.core.models import SignalInput, VILScoreObject
from app.core.routing import DEFAULT_THRESHOLDS, explain_route, route_signal
from app.core.scoring import DEFAULT_WEIGHTS, calculate_verifiability_score, calculate_vil_score, calculate_weighted_signal_score, infer_criteria_scores


def evaluate_signal(signal: SignalInput) -> VILScoreObject:
    criteria = infer_criteria_scores(signal)
    weighted = calculate_weighted_signal_score(criteria, DEFAULT_WEIGHTS)
    verifiability = calculate_verifiability_score(signal)
    final_score = calculate_vil_score(weighted, verifiability)
    route = route_signal(final_score, signal.risk_flags, DEFAULT_THRESHOLDS)
    reason = explain_route(route, final_score, signal.risk_flags)
    audit = create_audit_record(
        signal=signal,
        criteria_scores=criteria,
        weights=DEFAULT_WEIGHTS,
        thresholds=DEFAULT_THRESHOLDS,
        weighted_signal_score=weighted,
        verifiability_score=verifiability,
        vil_score=final_score,
        route=route,
        reason=reason,
        risk_flags=signal.risk_flags,
    )
    return VILScoreObject(
        signal_id=signal.signal_id,
        weighted_signal_score=weighted,
        verifiability_score=verifiability,
        vil_score=final_score,
        route=route,
        reason=reason,
        criteria_scores=criteria.as_dict(),
        risk_flags=signal.risk_flags,
        audit=audit,
    )
