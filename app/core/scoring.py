from __future__ import annotations

from typing import Dict

from app.core.models import CriteriaScores, SignalInput

DEFAULT_WEIGHTS: Dict[str, float] = {
    "strategic_alignment": 0.20,
    "revenue_potential": 0.20,
    "compounding_leverage": 0.15,
    "automation_potential": 0.15,
    "cognitive_load_reduction": 0.10,
    "urgency": 0.10,
    "source_quality": 0.05,
    "completeness": 0.05,
}

POSITIVE_TERMS = {
    "lead": ["budget", "urgent", "quote", "estimate", "paid", "contract", "client", "schedule"],
    "rfi": ["deadline", "impact", "change", "approval", "submittal", "schedule", "cost"],
    "content": ["trend", "audience", "proof", "case study", "distribution", "linkedin"],
    "support": ["blocked", "error", "customer", "production", "urgent", "failed"],
    "research": ["source", "evidence", "citation", "market", "benchmark", "risk"],
    "workflow_request": ["automation", "manual", "handoff", "approval", "routing", "admin"],
    "other": ["urgent", "revenue", "proof", "workflow", "risk", "client"],
}


def clamp(value: float, minimum: float = 0.0, maximum: float = 10.0) -> float:
    return max(minimum, min(maximum, value))


def calculate_weighted_signal_score(
    criteria_scores: CriteriaScores | Dict[str, float],
    weights: Dict[str, float] | None = None,
) -> float:
    """Calculate weighted signal value on a 0 to 10 scale."""
    weights = weights or DEFAULT_WEIGHTS
    scores = criteria_scores.as_dict() if isinstance(criteria_scores, CriteriaScores) else criteria_scores
    total = 0.0
    for criterion, weight in weights.items():
        total += clamp(float(scores.get(criterion, 0.0))) * float(weight)
    return round(clamp(total), 2)


def calculate_verifiability_score(signal: SignalInput) -> float:
    """Score how much evidence/context supports the signal.

    The score intentionally rewards concrete content, source pointers, structured metadata,
    and absence of unsupported critical-risk flags.
    """
    score = 2.0
    content = signal.content.strip()

    if len(content) >= 40:
        score += 1.5
    if len(content) >= 120:
        score += 1.0
    if signal.metadata:
        score += min(2.0, len(signal.metadata) * 0.4)
    if signal.source_pointers:
        score += min(2.0, len(signal.source_pointers) * 0.75)
    if signal.source and signal.source.lower() not in {"unknown", "n/a", "none"}:
        score += 1.0

    speculative_markers = ["maybe", "possibly", "guess", "heard", "rumor", "unverified"]
    if any(marker in content.lower() for marker in speculative_markers):
        score -= 1.0

    return round(clamp(score), 2)


def infer_criteria_scores(signal: SignalInput) -> CriteriaScores:
    """Infer deterministic baseline criteria scores from structured signal content.

    This is not an LLM scorer. It is a transparent rules-based default that clients can tune.
    """
    content = signal.content.lower()
    metadata_blob = " ".join(str(value).lower() for value in signal.metadata.values())
    text = f"{content} {metadata_blob}"
    terms = POSITIVE_TERMS.get(signal.signal_type, POSITIVE_TERMS["other"])
    hits = sum(1 for term in terms if term in text)
    base = clamp(3.0 + hits * 0.9)

    has_business_context = any(word in text for word in ["business", "company", "client", "contractor", "customer", "team"])
    has_money_context = any(word in text for word in ["revenue", "cost", "budget", "paid", "quote", "estimate", "sales"])
    has_automation_context = any(word in text for word in ["automation", "manual", "admin", "workflow", "routing", "handoff"])
    has_urgency_context = any(word in text for word in ["urgent", "deadline", "today", "blocked", "asap", "delay"])

    return CriteriaScores(
        strategic_alignment=base + (1.5 if has_business_context else 0),
        revenue_potential=base + (2.0 if has_money_context else 0),
        compounding_leverage=base + (1.0 if has_automation_context else 0),
        automation_potential=base + (2.0 if has_automation_context else 0),
        cognitive_load_reduction=base + (1.5 if any(w in text for w in ["admin", "manual", "repetitive", "weekend", "office"]) else 0),
        urgency=base + (2.0 if has_urgency_context else 0),
        source_quality=5.0 + (1.0 if signal.source_pointers else 0) + (1.0 if signal.source != "unknown" else 0),
        completeness=4.0 + min(4.0, len(signal.metadata) * 0.5) + (1.0 if len(signal.content) > 80 else 0),
    )


def calculate_vil_score(weighted_signal_score: float, verifiability_score: float) -> float:
    """Apply VIL verification cap."""
    return round(clamp(min(weighted_signal_score, verifiability_score)), 2)
