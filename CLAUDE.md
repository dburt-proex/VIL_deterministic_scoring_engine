# Claude Operating Instructions — VIL

Project: Verified Intelligence Layer (VIL)

VIL is a deterministic signal scoring, verification, routing, and audit layer for AI-assisted operations. It evaluates inbound signals before they consume operator attention or trigger downstream automation.

## Core invariant

```text
vil_score = min(weighted_signal_score, verifiability_score)
```

A signal cannot outrank its evidence. Do not weaken this invariant without an explicit product decision and regression tests.

## Default workflow

1. Classify the task: bug, feature, refactor, docs, release, scoring-policy, audit, dashboard, or infrastructure.
2. Identify risk: low, medium, or high.
3. Explore relevant files before editing.
4. Plan first for scoring, routing, audit, auth, persistence, dashboard, or API contract changes.
5. Implement in small logical units.
6. Verify with the narrowest useful command set.
7. Return exact commands run, results, changed files, remaining risks, and next action.

## Commands

Install:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run app:

```bash
uvicorn app.main:app --reload
```

Run tests:

```bash
pytest
```

Focused tests:

```bash
pytest -q
```

Smoke checks:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/config
curl http://localhost:8000/metrics
curl http://localhost:8000/audits
curl -X POST http://localhost:8000/score -H "Content-Type: application/json" -d @examples/lead_intake_signal.json
```

## Protected areas

Treat these as high-risk:

- scoring formula
- threshold routing
- risk override logic
- audit ledger writes
- API request / response contracts
- persistence model
- future auth / tenant isolation
- production deployment config

For protected areas, produce a plan before editing and include regression proof.

## Architecture rules

- Keep scoring deterministic and inspectable.
- Preserve route meanings: PASS, REVIEW, CLARIFY, ARCHIVE, HALT.
- Keep audit records append-oriented and explainable.
- Do not hide or smooth over evidence gaps.
- Prefer explicit scoring criteria over opaque model judgment.
- Any dashboard change must preserve API correctness.

## Completion contract

A task is not done until the final response includes:

- summary of change
- files changed
- verification commands run
- pass/fail result
- unresolved risks
- next recommended action

## Skill routing

Use project skills when relevant:

- `/repo-onboarding-map` before unfamiliar or multi-file work
- `/backend-api-architect` for API/service changes
- `/database-migration-governor` for persistence changes
- `/debug-root-cause` for failures
- `/test-verification-runner` before completion
- `/security-review-sentinel` for auth, data, dependencies, and infrastructure
- `/technical-docs-generator` after externally visible changes
- `/release-pr-manager` before PR or release notes

## Review rule

For any scoring, routing, audit, persistence, auth, or infrastructure change, use a reviewer agent or fresh context review before merge.
