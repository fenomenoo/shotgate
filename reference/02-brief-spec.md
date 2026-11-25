# 02 — The nine-block brief

The brief decides whether the video is good, far more than the model does. A strong model with a vague brief produces a montage of pretty scenes with no idea in it.

A brief missing any of these nine blocks produces a video that drifts. Fill all nine, every time. Use [../templates/brief.md](../templates/brief.md).

---

## 1. Style

Palette with **hex codes**, not adjectives. "Warm and friendly" means nothing; `#F2E8DC` background, `#1B2A33` ink, `#E4572E` accent means something.

Also specify: shapes and their corner radius, camera behaviour (static / slow push / snap cuts), texture (flat / grain / halftone), and a short **avoid** list ("no gradients, no drop shadows, no stock-photo people").

The avoid list is the highest-leverage line in the whole brief. Models over-decorate by default.

## 2. Characters

One paragraph per recurring character: silhouette, proportions, clothing, colours, and **what they never do**. Written once, reused every episode, so the character looks the same in shot 1 and shot 40.

For non-character formats, write the equivalent: the recurring diagram, the recurring hand, the recurring texture. Consistency of *any* visual anchor is what makes a page recognisable in a feed.

Use [../templates/series-bible.md](../templates/series-bible.md) as the master copy. Never restate characters from memory.

## 3. Shot list

A table: `# | start | end | duration | composition | on-screen text | camera | transition`.

Rules:
- **Every shot a different composition.** Two shots with the same framing is a pacing failure.
- No shot longer than ~3s without an internal event.
- Write the composition, not the content — "wide, subject left third, text block right" beats "show the app".

## 4. Twist and ending beat

Not a summary. The brief must state the turn — the moment the video changes direction — and the final beat that lands on screen.

If you cannot write the twist in one sentence, you do not have a video yet, you have a topic.

## 5. Sound

- Music: mood, tempo band (BPM), and 2–3 reference tracks by feel.
- Effects: each one with a timestamp and what it is for (whoosh on cut, tick on number reveal, low hit on the turn).
- Silence: at least one deliberate silence. It is the cheapest retention tool that exists.

## 6. Pacing

The measurable version, not the adjective:

- a new visual event approximately **every 0.5s**
- **hard cuts**, not dissolves
- **nothing static longer than 1s**
- first 1.5s contains a full hook (see `04-hooks.md`)

`contactsheet.py` enforces the static-frame part mechanically. If two adjacent frames in the sheet look alike, the gate fails.

## 7. Source of truth

Every number, date, name, price, percentage and claim that may appear on screen, written as plain text in `templates/source-of-truth.md`.

**No entry, no claim.** `claims.py` checks the script against this file and fails on any number in the script that is not in the source. The point is not verification — it is making fabrication mechanically impossible rather than merely discouraged.

## 8. Hard rules

Copy the standing list into every brief so the renderer sees it:

- no real faces
- no logos without written rights
- no frames from other creators
- no medical, financial or earnings guarantees
- AI disclosure where required
- sound-off readable: every claim legible without audio

## 9. Quality bar

Three lines, stated numerically:

- hook fully delivered inside **1.5s**
- readable with **sound off**
- **fix the 3 weakest shots before delivering** — name them in the approval

---

## Voiceover arithmetic

Write to words, not to feeling: **~2.3 words/second**. A 30s video is 65–75 words. A 45s video is 100–110.

Write the VO first, then time the shots to it. Doing it the other way produces rushed narration and dead air.

## What a bad brief looks like

> "A fun, modern explainer about our app, energetic music, showing the features."

That brief cannot fail, because it cannot be checked. Which is why it produces a video nobody can explain the failure of.

## What a good brief looks like

Nine filled blocks, a shot table with times and compositions, a twist in one sentence, a source-of-truth file with four entries, and an avoid list. It should take 15–25 minutes to write the first time and about 6 minutes once the series bible exists.
