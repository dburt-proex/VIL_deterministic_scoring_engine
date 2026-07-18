# Claude Hooks — VIL

This folder contains conservative Claude Code hook scripts for the VIL repo.

## Active hook

- `block-destructive.sh`: blocks destructive shell operations before execution.

## Deferred hook candidates

These are intentionally not wired yet:

- focused test runner after edits
- completion gate requiring verification evidence
- secret scan before commit

Keep hooks conservative. If a rule is advisory, put it in `CLAUDE.md` or a skill. If a rule must never be skipped, implement it here and wire it through `.claude/settings.json`.
