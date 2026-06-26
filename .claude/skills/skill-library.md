# VIL Claude Skill Library

This file stores the install-ready Claude workflows for VIL. If your Claude Code setup supports per-skill folders, split each section into `.claude/skills/<skill-name>/SKILL.md`.

## 1. Claude System Bootstrap

Use before serious VIL work. Read README.md and CLAUDE.md, classify the task, identify risk, choose the workflow, and return a verification checklist.

## 2. Repo Onboarding Mapper

Use before unfamiliar or multi-file work. Map entrypoints, scoring flow, routing flow, audit flow, dashboard flow, tests, and unknowns without editing files.

## 3. Product Spec Interviewer

Use before building vague features. Convert intent into SPEC.md with scope, non-goals, acceptance criteria, affected files, and proof-of-done.

## 4. Backend API Architect

Use for API, service, scoring, routing, or audit changes. Define request/response contracts, error behavior, tests, and verification commands.

## 5. Database Migration Governor

Use before persistence, audit storage, schemas, indexes, backfills, or tenant data work. Require rollback and validation queries.

## 6. Debug Root-Cause Investigator

Use for failing tests, regressions, broken routes, API errors, or dashboard issues. Reproduce first, isolate root cause, fix minimally, and verify.

## 7. Test Verification Runner

Use before claiming work is done. Run the narrowest useful command set and report exact commands, results, and unresolved risk.

## 8. Security Review Sentinel

Use for auth, data exposure, audit privacy, dependencies, secrets, and infrastructure. Return severity-ranked findings and fixes.

## 9. Refactor Planner

Use for behavior-preserving structure improvements. Name invariants, affected files, rollback path, and verification commands before editing.

## 10. ML Evaluation Designer

Use for rubric, prompt QA, scoring evals, and AI workflow checks. Define criteria, test cases, gold examples, failure taxonomy, and pass thresholds.

## 11. Technical Docs Generator

Use after implementation. Update README, API examples, operator notes, demo notes, and maintenance guidance.

## 12. Release and PR Manager

Use before PRs or releases. Produce commit message, PR body, verification evidence, risk summary, rollout notes, and rollback notes.

## 13. Prompt Instruction Compiler

Use to convert rough prompts into executable prompts, repo rules, agent prompts, or reusable workflow files.

## 14. Agent Orchestration Designer

Use to design multi-agent workflows with roles, inputs, outputs, handoffs, permissions, and verification gates.
