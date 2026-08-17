# VIL Compliance Readiness Baseline

Status: REVIEW  
Assessment date: 2026-08-16  
Canonical control registry: `dburt-proex/casa/governance/CONTROL-REGISTRY.yaml` v0.1

## Claim boundary

VIL may claim deterministic signal scoring, evidence-capped routing and audit logging where supported. It must not claim ISO/IEC certification, SOC 2 attestation or full compliance without independent assurance.

## Scope

VIL is assessed as the deterministic intake/scoring/routing layer: normalization, value scoring, verifiability scoring, critical-risk overrides, route decisions, audit records and supporting agent/test safeguards.

## Evidence-backed strengths

- Explicit deterministic scoring invariant: a signal cannot outrank its evidence.
- Defined PASS/REVIEW/CLARIFY/ARCHIVE/HALT routes.
- Persistent audit logging and audit API surface.
- Risk override logic and regression tests.
- Repository-local destructive-action blocking and security/test agent profiles.

## Gap register

| Priority | Control | Gap | Closure evidence |
|---|---|---|---|
| P0 | IAM-001 | Authentication/access control absent from current paid-deployment baseline | auth implementation + privilege matrix + access-review record |
| P0 | INC-001 | Incident response absent | IR SOP + tabletop + RCA + corrective-action/retest records |
| P0 | DAT-001 | Data governance and tenant storage controls incomplete | data inventory/classification/retention/deletion policy + tenant isolation evidence |
| P0 | SUP-001 | Supplier/model-provider governance absent | supplier inventory + risk assessment + approved-use review |
| P0 | BCM-001 | Backup/recovery controls absent | backup policy + successful restore test + recovery receipt |
| P1 | GOV-001 | VIL routing is not organization-level governance authority | authority/scope/approval policy binding |
| P1 | CHG-001 | Change-control evidence incomplete | PR/CI gate + review receipt + commit evidence |
| P1 | SEC-001 | No formal threat model | threat model + negative tests + security review |
| P1 | AI-001 | Full AI lifecycle records absent | AI inventory + intended use + TEVV + monitoring + retirement evidence |
| P1 | REV-001 | Tests are not recurring internal audit/management review | audit report + management review + CAPA status |

## Validation workflow

1. Resolve manifest evidence paths against the assessed commit.
2. Execute `pytest` and any configured CI in an authorized environment.
3. Capture test output, audit-ledger behavior and route fixtures as canonical CASA evidence receipts.
4. Verify critical-risk override and evidence-cap invariants with negative-path tests.
5. Close or formally accept P0 risks.
6. Conduct internal readiness review before external assurance.

## Phase 10 entry criteria

External assurance is blocked until P0 findings are closed or formally risk-treated, exact applicable framework requirements are mapped, evidence retention is established and management/operator review is recorded.
