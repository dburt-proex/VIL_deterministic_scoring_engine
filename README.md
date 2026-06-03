# Verified Intelligence Layer

Deterministic signal scoring, verification, routing, and audit records for AI-assisted operations.

VIL evaluates inbound signals before they consume operator attention or trigger downstream automation. It turns messy leads, RFIs, research items, support issues, content opportunities, and workflow requests into structured score objects with clear routing decisions.

## Core Question

> Is this signal worth acting on, reviewing, clarifying, archiving, or halting?

## Flow

```text
Raw Signal -> Normalize -> Score Value -> Score Verifiability -> Apply Risk Overrides -> Route -> Audit
```

## Routes

| Route | Meaning |
|---|---|
| PASS | High-confidence signal. Ready for downstream action. |
| REVIEW | Valuable or plausible signal requiring human judgment. |
| CLARIFY | Potentially useful, but missing evidence or specificity. |
| ARCHIVE | Low-value noise. Store or discard. |
| HALT | Unsafe, non-compliant, destructive, or outside scope. |

## Scoring Invariant

```text
vil_score = min(weighted_signal_score, verifiability_score)
```

A signal cannot outrank its evidence.

## Default Criteria

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

## Thresholds

| Score | Route |
|---:|---|
| 8.0 to 10.0 | PASS |
| 5.0 to 7.99 | REVIEW |
| 3.0 to 4.99 | CLARIFY |
| 0.0 to 2.99 | ARCHIVE |
| Critical risk flag | HALT |

## API

```bash
uvicorn app.main:app --reload
```

```bash
curl http://localhost:8000/health
```

```bash
curl -X POST http://localhost:8000/score -H "Content-Type: application/json" -d @examples/lead_intake_signal.json
```

## Install

```bash
git clone https://github.com/dburt-proex/VIL_deterministic_scoring_engine.git
cd VIL_deterministic_scoring_engine
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Docker

```bash
docker compose up --build
```

## Test

```bash
pytest
```

## Relationship to CASA

```text
VIL  = Should this signal move forward?
CASA = Is the proposed action allowed to execute?
```

VIL operates before execution. CASA governs execution.

## Commercial Wedge

First sellable service:

> AI Workflow Intake and Risk/Value Routing Audit

Best use cases: lead qualification, construction RFI triage, support prioritization, research intake, workflow pre-checking, agency request routing, and content opportunity scoring.
