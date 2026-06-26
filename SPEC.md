# SPEC — Claude Operating Layer for VIL

## Objective

Install a repo-native Claude operating layer for the Verified Intelligence Layer so Claude Code can work inside the project with stronger context discipline, repeatable workflows, specialist review, and evidence-based completion.

## Scope

Add:

- root `CLAUDE.md`
- root `SPEC.md`
- root `PLAN.md`
- root `AGENTS.md`
- `.claude/settings.json`
- `.claude/skills/*/SKILL.md`
- `.claude/agents/*.md`
- `.claude/hooks/*.sh`

## Non-goals

- Do not change VIL scoring logic.
- Do not alter API behavior.
- Do not add runtime dependencies.
- Do not change dashboard UI.
- Do not change tests.

## Acceptance criteria

- Repo has a clear Claude operating structure.
- VIL-specific rules preserve deterministic scoring and evidence-capped routing.
- Skills are ordered around high-value engineering workflows.
- Agents are scoped for review and research.
- Hooks are conservative and do not mutate application code.
- The PR is reviewable as documentation/configuration only.

## Proof of done

- File tree contains the Claude operating layer.
- Root `CLAUDE.md` names VIL invariants, commands, protected areas, and completion contract.
- Skills contain SKILL.md-ready instructions.
- Agents contain bounded roles and outputs.
- Hook scripts are present and safe-by-default.
