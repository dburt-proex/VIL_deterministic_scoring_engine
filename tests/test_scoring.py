from app.core.models import CriteriaScores, SignalInput
from app.core.scoring import calculate_verifiability_score, calculate_vil_score, calculate_weighted_signal_score


def test_weighted_score_uses_weights():
    scores = CriteriaScores(
        strategic_alignment=10,
        revenue_potential=10,
        compounding_leverage=0,
        automation_potential=0,
        cognitive_load_reduction=0,
        urgency=0,
        source_quality=0,
        completeness=0,
    )
    assert calculate_weighted_signal_score(scores) == 4.0


def test_vil_score_uses_verification_cap():
    assert calculate_vil_score(9.2, 5.4) == 5.4


def test_verifiability_rewards_context():
    signal = SignalInput(
        source="website_form",
        signal_type="lead",
        content="A contractor provided detailed context about admin bottlenecks, estimate follow-up delays, and lead routing needs.",
        metadata={"industry": "construction", "location": "Rochester"},
        source_pointers=[{"type": "form", "value": "website intake"}],
    )
    assert calculate_verifiability_score(signal) >= 6.0
