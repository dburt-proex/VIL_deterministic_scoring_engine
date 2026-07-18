#!/usr/bin/env bash
set -euo pipefail

if ! command -v jq >/dev/null 2>&1; then
  exit 0
fi

COMMAND="$(jq -r '.tool_input.command // ""')"

if echo "$COMMAND" | grep -Eiq '(rm[[:space:]]+-rf|git[[:space:]]+reset[[:space:]]+--hard|git[[:space:]]+clean[[:space:]]+-[a-zA-Z]*f|git[[:space:]]+push[[:space:]].*--force|dropdb|DROP[[:space:]]+DATABASE|DROP[[:space:]]+TABLE)'; then
  jq -n --arg reason "Blocked destructive command in VIL Claude operating layer: $COMMAND" '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: $reason
    }
  }'
  exit 0
fi

exit 0
