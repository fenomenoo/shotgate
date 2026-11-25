# 07 — Cost and the envelope

Most published pipelines describe a process and never state what it costs. That omission is how people end up with a working pipeline and a losing business. The point of routing is not elegance — it is unit economics.

## The envelope

Set a **cost ceiling per published video** before you start, and enforce it in the brief.

Example envelope for one 40s video:

| Line | Ceiling |
|---|---|
| brief + script (frontier model) | ~$0.30 |
| render code (helper model) | ~$0.10 |
| generative shots (2 of 12, hook + turn) | ~$2.00 |
| voiceover | ~$0.60 |
| music | ~$0.30 |
| compute (render + encode) | ~$0.05 |
| **total** | **~$3.35** |

A $3.35 video that gets 40k views and 30 installs is a business. A $158 video is a portfolio piece unless it lands very hard. Both are legitimate — but choose deliberately, not accidentally.

## Model routing

Route by *role*, not by habit:

| Role | Model tier | Why |
|---|---|---|
| Pick format, write brief, write hook | frontier | judgment; this is where quality is decided |
| Write the shot table and on-screen text | mid | structural, checkable |
| Write the render code (HTML/three.js/Remotion) | mid, escalate per shot | most shots are mechanical; the hard ones are worth frontier |
| Generate the cinematic shot | generative video | different substrate, not a text model at all |
| QA narration of stills ("is this cut off?") | mid with vision | cheap perception, human confirms |
| Claims check, format checks | **no model** | deterministic scripts are cheaper and cannot hallucinate |

The published $158 figure is a frontier model used for everything. That is a routing failure, not an inherent cost of the format.

## Three levers, in order of impact

1. **Component reuse.** A shot built from an existing parameterised component costs compute only. If 80% of shots are reused, you have removed 80% of the expensive steps. See `05-components.md`.
2. **Substrate routing.** Generative shots are the cost spike. Two per video, placed at the hook and the turn, where they pay for themselves. Everything else is code.
3. **Cache and re-render.** Deterministic builds mean an unchanged shot never re-renders. A QA fix on shot 7 costs one shot, not a rebuild.

## The ledger

Every video gets a row in `templates/video-log.csv`, and `scripts/cost.py` rolls it up:

- cost per video
- **cost per 1,000 views**
- **cost per install**
- revenue or estimated value per install, where known
- **margin ratio** — installs × value ÷ cost

The third and fifth numbers are the ones that tell you whether to scale. Cost per video is a vanity number; cost per install is the business.

## The rule that keeps you honest

**A format that costs more per install than it earns gets cut, regardless of how good it looks.**

That is the same rule as the kill criterion in `09-retention-loop.md`, applied to money instead of clicks. Together they are the whole reason to keep a ledger.

## Where people get this wrong

- Optimising cost per video before optimising cost per install. A cheap video nobody installs from is expensive.
- Not counting compute. Render farms and GPU time are real, small, and always forgotten.
- Forgetting the cost of *your* three minutes. At any real hourly rate, human minutes dominate the ledger — which is why the human budget is capped at 3 minutes rather than left open.
