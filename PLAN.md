# PLAN — Claude Operating Layer Rollout

## Phase 1 — Repo memory

- Add `CLAUDE.md` with VIL invariants, commands, protected areas, and completion contract.
- Keep the file concise and stable.
- Move procedures into skills instead of bloating root memory.

## Phase 2 — Skills

Install reusable workflows under `.claude/skills/`:

1. claude-system-bootstrap
2. repo-onboarding-map
3. product-spec-interviewer
4. backend-api-architect
5. database-migration-governor
6. debug-root-cause
7. test-verification-runner
8. security-review-sentinel
9. refactor-planner
10. ml-eval-designer
11. technical-docs-generator
12. release-pr-manager
13. prompt-instruction-compiler
14. agent-orchestration-designer

## Phase 3 — Specialist agents

Install read-only or review-first agents:

- security-reviewer
- architecture-reviewer
- test-verifier
- database-governor
- docs-writer
- research-mapper

## Phase 4 — Hooks

Install conservative hook scripts:

- block destructive shell commands
- run focused verification opportunistically after edits
- require verification evidence as an optional completion gate

## Phase 5 — Usage workflow

Recommended command sequence for future VIL work:

```text
/repo-onboarding-map
/product-spec-interviewer
/backend-api-architect or /debug-root-cause
/test-verification-runner
/security-review-sentinel
/release-pr-manager
```

## Merge criteria

- Documentation/config files only.
- No app behavior changes.
- No scoring or routing changes.
- PR body explains how to use the new system.
