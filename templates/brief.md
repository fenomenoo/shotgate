# Brief — EP{NNN} / {page}

> Fill all nine blocks. A brief missing a block produces a video that drifts.
> Time budget: ~15 min first time, ~6 min once the series bible exists.

**Page:** `{page}` · **Format:** `{format}` · **Substrate:** `{primary}` + `{accent}`
**Hook family:** `{#} {name}` · **Target length:** `{30|40|45}s` · **VO words:** `{~70}`

---

## 1. Style

- Palette: bg `#______` · ink `#______` · accent `#______` · secondary `#______`
- Shapes: {radius, stroke weight, flat/halftone/grain}
- Camera: {static | slow push | snap cuts | handheld-substitute}
- Type: {family, weight, tracking, uppercase y/n}
- **Avoid:** {e.g. gradients, drop shadows, stock-photo people, lens flares, rounded everything}

## 2. Characters / recurring anchors

> Copy from the series bible. Do not restate from memory.

**{Name}** — {one paragraph: silhouette, proportions, clothing, colours, expression range}.
**Never:** {what they never do}.
**Anchor:** {the recurring diagram / hand / texture / grid that appears in every episode}

## 3. Shot list

| # | start | end | dur | composition | on-screen text | camera | transition |
|---|---|---|---|---|---|---|---|
| 1 | 0.0 | 1.5 | 1.5 | | | | |
| 2 | 1.5 | 4.0 | 2.5 | | | | |
| 3 | 4.0 | 7.0 | 3.0 | | | | |
| … | | | | | | | |

- Every shot a different composition.
- No shot over 3s without an internal event.
- Write composition, not content.

## 4. Twist / ending beat

**The turn (one sentence):** {the moment the video changes direction}

**Final beat:** {the last thing on screen, one line}

## 5. Sound

- Music: {mood}, {BPM band}, refs: {track feel}
- Effects: {timestamp} → {effect} → {purpose}
- Silence: {timestamp} → {why}

## 6. Pacing

- visual event every ~0.5s · hard cuts · nothing static > 1s
- hook complete by 1.5s
- gate target: no two adjacent contact-sheet frames alike

## 7. Source of truth

> Every number/date/claim that may appear on screen. No entry, no claim.

| claim | value | source |
|---|---|---|
| | | |

Full file: `briefs/EP{NNN}.source.md`

## 8. Hard rules

- [ ] no real faces
- [ ] no logos without written rights
- [ ] no third-party frames
- [ ] no medical/financial/earnings guarantee
- [ ] AI disclosure flag set on every platform
- [ ] readable with sound off

## 9. Quality bar

- hook fully delivered inside 1.5s
- readable with sound off
- **3 weakest shots named and fixed before delivery:**
  1. {shot #} — {why}
  2. {shot #} — {why}
  3. {shot #} — {why}

---

## Approval

- [ ] script approved by a human (~2 min)
- [ ] rendered
- [ ] `python scripts/gate.py` → exit 0
- [ ] contact sheet read by a human (~1 min)
- [ ] posted with per-video link
