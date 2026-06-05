# Routing Logic

VIL routes every scored signal into one of five states.

## States

| Route | Meaning |
|---|---|
| PASS | Ready for downstream action. |
| REVIEW | Worth human judgment before action. |
| CLARIFY | Missing context, evidence, or specificity. |
| ARCHIVE | Low-confidence or low-value noise. |
| HALT | Critical risk or boundary violation. |

## Thresholds

```text
8.0 to 10.0  -> PASS
5.0 to 7.99  -> REVIEW
3.0 to 4.99  -> CLARIFY
0.0 to 2.99  -> ARCHIVE
critical risk -> HALT
```

## Override Rule

HALT overrides score.

A signal with a high score still routes to HALT when a critical risk flag is present.
