---
name: shotgate
description: Run a faceless short-form video pipeline end to end — pick the format from the audience, write a production brief the model cannot drift from, route each shot to the right renderer, and gate the output with real automated checks (resolution, loudness, pacing, dead frames, unverified claims) before anything is posted. Also closes the loop: retention curves and per-video attribution feed back into the next brief. Use when someone asks to make, plan, systematise, QA or scale short-form video content, faceless/theme pages, AI video series, explainer or motion-graphics videos, or asks why their videos get views but no installs.
---

# shotgate

A faceless video pipeline where the **gate** is the product, not the renderer.

Most "AI video" workflows automate production and leave judgment to vibes. Shotgate automates the part that is cheap to automate (rendering, formatting, checking) and forces the part that decides success (format choice, brief, hook) into an explicit artifact you approve in minutes.

**Human budget: 3 minutes per video.** Approve the script (2 min), read the contact sheet (1 min), post. If the loop is taking longer, something upstream is wrong.

## The loop

```
FORMAT → BRIEF → RENDER → GATE → POST → LEARN ↺
  ↑__________________________________________|
```

Never skip GATE. Never post a video the gate did not pass. Never run LEARN less than weekly.

## Phase 1 — FORMAT

The format comes from the *user*, not the tool. Answer three questions in writing before touching a renderer:

1. What does this person already watch, before they know they need us?
2. Does the product have to be **seen working**, or **understood**?
3. Who has to trust it — someone scrolling at 11pm, or a buyer evaluating at work?

Then read [reference/01-format-decision.md](reference/01-format-decision.md) and commit to **one main style per page**, plus one style under test.

Rule: a new style gets a new page or its own series. Never mix styles on one page.

## Phase 2 — BRIEF

Read [reference/02-brief-spec.md](reference/02-brief-spec.md). Copy [templates/brief.md](templates/brief.md) and fill all nine blocks. A brief missing any block produces a video that drifts.

The two blocks people skip and always regret:

- **Source of truth** — every number, date, name and claim that will appear on screen, written as plain text. The claims linter checks the script against this file mechanically. No source entry, no claim on screen.
- **Pacing** — a new visual event roughly every 0.5s, hard cuts, nothing static longer than 1s. Slow illustrative videos die in the first 1.5 seconds.

Voiceover: ~2.3 words per second. 30s ≈ 65–75 words. Write to that number, do not discover it.

## Phase 3 — RENDER

Do **not** default to one renderer. Route per shot — see [reference/03-renderers.md](reference/03-renderers.md). Code rendering (HTML/three.js/Remotion → Playwright → ffmpeg) is excellent for text, data, motion graphics, explainers. It is structurally bad at character acting, painted texture, cinematic realism and anything a face has to carry. Use the right substrate per shot and assemble on one timeline.

Deterministic rule: every frame must be a pure function of `t`. Then one bad shot re-renders alone without disturbing anything else.

## Phase 4 — GATE

This is the part that does not exist in most workflows. One command:

```bash
python scripts/gate.py --video out/EP012.mp4 --brief briefs/EP012.md --script out/EP012.txt
```

It runs, in order:

| Check | Catches |
|---|---|
| `qa.py` — ffprobe + EBU R128 | wrong resolution/fps/duration, missing audio, quiet audio |
| `contactsheet.py` — 24-frame grid + similarity | dead pacing, repeated frames, cut-off text |
| `stills.py` — key timestamps | empty frames, overlaps, unreadable text |
| `claims.py` — script vs source of truth | invented numbers, dates, percentages |

Exit code 1 means **do not post**. Fix, re-render only the failing shot, run gate again.

Agent rule: read the contact sheet and the stills yourself. If two adjacent frames look the same, the pacing is too slow — that is a gate failure, not a style choice.

## Phase 5 — POST

- One video per page per day, at the page's learned post hours.
- Each platform gets its own caption and cover frame.
- **AI disclosure flags set on every platform.** Non-negotiable, see [reference/06-compliance.md](reference/06-compliance.md).
- **A unique link per video**, not per page. A per-page link only proves the page works; a per-video link proves which video produced the install. See [reference/08-attribution.md](reference/08-attribution.md).

## Phase 6 — LEARN

Weekly, not daily:

1. Pull retention curves per video. Run `python scripts/retention.py`.
2. Log views, shares, saves, link clicks, installs in [templates/video-log.csv](templates/video-log.csv).
3. Compute per-format chain: views → profile visits → link clicks → installs → paid.
4. Rewrite the brief for next week's batch using the retention feedback — which hook shape held, which shot pattern lost them.
5. Apply the kill/scale rule (below) without sentiment.

Details: [reference/09-retention-loop.md](reference/09-retention-loop.md).

## Kill and scale

Write these numbers down before you start, or you will run this for three months and learn nothing.

- **Kill:** a format with a `< 0.5%` link click-through rate over its last 20 videos, regardless of view count.
- **Scale:** a format beating your median installs-per-1k-views by 2× gets 3× the output volume next cycle.
- **Hold:** everything else. Hold does not mean ignore — it means do not multiply.

## Hard rules

1. No real faces. No logos you do not have written rights to. No frames from other creators.
2. No number, date or percentage on screen that is not in the source-of-truth file.
3. No claim that reads as guaranteed medical, financial or earnings advice. The claims linter is a floor, not a legal review.
4. Every video discloses AI generation where the platform requires it.
5. Nothing posts that the gate has not passed.
6. One style per page. One page per brand. One link per video.

## Files

```
reference/01-format-decision.md   pick the format from the audience
reference/02-brief-spec.md        the nine-block brief, block by block
reference/03-renderers.md         per-shot renderer routing matrix
reference/04-hooks.md             40 named hook patterns
reference/05-components.md        reusable scene components + versioning
reference/06-compliance.md        AI disclosure, music rights, claims
reference/07-cost.md              model routing and the cost envelope
reference/08-attribution.md       per-video links and the install chain
reference/09-retention-loop.md    retention → brief feedback
templates/brief.md                fill-in brief
templates/series-bible.md         recurring character + style lock
templates/source-of-truth.md      verified facts only
templates/video-log.csv           the ledger
scripts/gate.py                   one-command gate (runs all checks)
scripts/qa.py                     ffprobe + loudness + duration
scripts/contactsheet.py           24-frame grid + pacing similarity
scripts/stills.py                 key-timestamp stills
scripts/claims.py                 script vs source-of-truth linter
scripts/retention.py              retention drop-off scorer
scripts/cost.py                   cost ledger and rollup
```

Install: nothing. Python 3.9+, `ffmpeg`/`ffprobe` on PATH, `pillow`. Scripts are stdlib + Pillow only.
