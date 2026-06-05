# VIL Scoring Engine

The scoring engine converts inbound operational signals into deterministic score objects.

## Core Invariant

```text
vil_score = min(weighted_signal_score, verifiability_score)
```

The final score is capped by verifiability. A valuable-looking signal cannot receive a high final score when evidence is weak.

## Weighted Signal Score

The weighted score estimates operational and commercial value.

```text
weighted_signal_score = sum(criteria_score * criterion_weight)
```

Default weights:

| Criterion | Weight |
|---|---:|
| strategic_alignment | 0.20 |
| revenue_potential | 0.20 |
| compounding_leverage | 0.15 |
| automation_potential | 0.15 |
| cognitive_load_reduction | 0.10 |
| urgency | 0.10 |
| source_quality | 0.05 |
| completeness | 0.05 |

## Verifiability Score

The verifiability score estimates whether the signal has enough support to move forward.

Signals score higher when they include:

- Specific content
- Structured metadata
- Source pointers
- Known source
- Concrete operational or commercial context

Signals score lower when they are vague, speculative, or unsupported.

## Risk Overrides

Critical flags override normal scoring and route the signal to HALT.

Examples:

- secrets
- policy_violation
- unsafe_action
- irreversible_external_action
- private_data_exposure

## Output

Each evaluation returns:

- weighted_signal_score
- verifiability_score
- vil_score
- route
- reason
- criteria_scores
- risk_flags
- audit record
