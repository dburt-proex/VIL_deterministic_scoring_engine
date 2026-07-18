# AGENTS — VIL Specialist Review System

Use these agents to keep the main Claude session clean and force independent review of high-risk changes.

## security-reviewer

Use for auth, tenant isolation, secrets, dependencies, API exposure, data handling, and infrastructure.

Output:

- severity-ranked findings
- affected files
- exploit path or failure mode
- recommended fix
- verification command

## architecture-reviewer

Use for scoring flow, routing boundaries, dashboard/API separation, and module structure.

Output:

- boundary assessment
- coupling risks
- invariant risks
- simpler architecture option
- recommended diff constraints

## test-verifier

Use before merging any change that claims behavior is correct.

Output:

- tests that prove the requirement
- tests that are missing
- weak assertions
- focused commands to run
- confidence rating

## database-governor

Use before persistence, audit storage, tenant isolation, indexes, schemas, or migrations.

Output:

- forward plan
- rollback plan
- data risk
- lock/performance risk
- validation queries

## docs-writer

Use after externally visible changes.

Output:

- README update
- API examples
- operator notes
- change summary
- commercial demo notes

## research-mapper

Use before unfamiliar multi-file work.

Output:

- entrypoints
- call graph
- data flow
- affected files
- unknowns
- recommended next step
