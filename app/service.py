from app.core.audit import create_audit_record
from app.core.models import Route, SignalInput, VILScoreObject
from app.core.routing import DEFAULT_THRESHOLDS, explain_route, route_signal
from app.core.scoring import DEFAULT_WEIGHTS, calculate_verifiability_score, calculate_vil_score, calculate_weighted_signal_score, infer_criteria_scores


def _content_preview(content: str, limit: int = 180) -> str:
    normalized = " ".join(content.split())
    if len(normalized) <= limit:
        return normalized
    return f"{normalized[: limit - 1].rstrip()}…"


def recommend_action(route: Route) -> str:
    actions = {
        Route.PASS: "Move to the next workflow step with the audit record attached.",
        Route.REVIEW: "Assign to an operator before outreach, execution, or handoff.",
        Route.CLARIFY: "Request missing context, source evidence, or decision ownership before routing.",
        Route.ARCHIVE: "Archive as low-confidence noise unless stronger proof appears.",
        Route.HALT: "Pause the workflow, escalate the record, and require explicit authority before action.",
    }
    return actions[route]


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
        source=signal.source,
        signal_type=signal.signal_type,
        content_preview=_content_preview(signal.content),
        weighted_signal_score=weighted,
        verifiability_score=verifiability,
        vil_score=final_score,
        route=route,
        reason=reason,
        recommended_action=recommend_action(route),
        criteria_scores=criteria.as_dict(),
        risk_flags=signal.risk_flags,
        audit=audit,
    )
