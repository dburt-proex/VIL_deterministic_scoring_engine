from __future__ import annotations

from typing import Dict, Iterable, List

from app.core.models import Route

DEFAULT_THRESHOLDS: Dict[str, float] = {
    "pass": 8.0,
    "review": 5.0,
    "clarify": 3.0,
    "archive": 0.0,
}

DEFAULT_HALT_FLAGS = {
    "secrets",
    "prod_data_destruction",
    "policy_violation",
    "unsafe_action",
    "irreversible_external_action",
    "regulated_decision",
    "private_data_exposure",
}


def has_halt_flag(risk_flags: Iterable[str], halt_flags: Iterable[str] | None = None) -> bool:
    halt_set = {flag.lower() for flag in (halt_flags or DEFAULT_HALT_FLAGS)}
    return any(str(flag).lower() in halt_set for flag in risk_flags)


def route_signal(
    vil_score: float,
    risk_flags: List[str] | None = None,
    thresholds: Dict[str, float] | None = None,
    halt_flags: Iterable[str] | None = None,
) -> Route:
    risk_flags = risk_flags or []
    thresholds = thresholds or DEFAULT_THRESHOLDS

    if has_halt_flag(risk_flags, halt_flags):
        return Route.HALT
    if vil_score >= thresholds["pass"]:
        return Route.PASS
    if vil_score >= thresholds["review"]:
        return Route.REVIEW
    if vil_score >= thresholds["clarify"]:
        return Route.CLARIFY
    return Route.ARCHIVE


def explain_route(route: Route, vil_score: float, risk_flags: List[str] | None = None) -> str:
    risk_flags = risk_flags or []
    if route == Route.HALT:
        return f"HALT triggered by critical risk flags: {', '.join(risk_flags) or 'unspecified critical risk'}."
    if route == Route.PASS:
        return f"Signal scored {vil_score}. It is high-confidence and ready for downstream action."
    if route == Route.REVIEW:
        return f"Signal scored {vil_score}. It appears valuable but requires human judgment before action."
    if route == Route.CLARIFY:
        return f"Signal scored {vil_score}. It may be useful but lacks enough evidence, context, or specificity."
    return f"Signal scored {vil_score}. It is low-value or low-confidence noise and should be archived."
