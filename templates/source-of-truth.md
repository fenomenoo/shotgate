# Source of truth — EP{NNN}

Every number, date, name, price and claim that may appear on screen. `scripts/claims.py` checks the narration script against this file and fails on any number it cannot find here.

**Rule: no entry, no claim.**

## Verified facts

| # | claim | value (exact) | source | checked |
|---|---|---|---|---|
| 1 | | | {url / document / measurement} | {date} |
| 2 | | | | |
| 3 | | | | |

## Allowed phrasings

Exact strings the script may use, where wording matters:

- "…"
- "…"

## Explicitly not claimed

Things that are true-ish but that you will not say, because they cannot be evidenced:

- {e.g. "doubles your savings" — no data}
- {e.g. "faster than {competitor}" — no benchmark}

## Notes

- Dates in {format}; write years in full.
- Percentages to one decimal.
- Currency: {code, symbol placement}.
