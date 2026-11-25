# 05 — The component library

"Keep a style library" is usually written as advice and implemented as a folder of screenshots nobody opens. Make it actual, parameterised, versioned components instead. Then a new video is mostly *reuse* plus one new element, which is the biggest simultaneous quality and cost lever available.

## Why components beat templates

A template is a whole video you fill in. It gets stale and every video looks the same.

A component is a **shot primitive** with parameters. A dozen components compose into thousands of distinct videos that still look like the same page.

```
scene: number_reveal
  params: { value, prefix, suffix, accent, bg, hold_ms, enter: "snap"|"rise"|"type" }
```

That one component covers a price, a percentage, a countdown and a statistic — and every use has the same motion language, so the page feels authored rather than assembled.

## Naming

`<category>.<variant>` — lowercase, stable, never renamed once used:

```
type.kicker          small overline text
type.headline        big statement, word-by-word pop
type.stat             number with label
type.compare         two values, diff highlighted
motion.wipe          hard directional cut
motion.slam          object enters and stops
diagram.node          labelled circle
diagram.flow          node → node with arrow logic
chart.line            line with reveal sweep
chart.bar             bar race or grow
ui.callout            highlight box on screen capture
character.idle        recurring character, neutral pose
character.react       recurring character, reaction
end.card              logo-free end card with one CTA line
```

## The 80/20 rule

Aim for: **80% of a video's shots are existing components with new parameters; 20% is one new component or one new generative shot.**

If a video needs 100% new components, it is a new style — put it on a new page, per `01-format-decision.md`.

This is also the cost story. Reusing components costs nothing to render beyond compute. Regenerating everything with a frontier model every time is how you end up with a $158 reel.

## Versioning, like software

Every video is a build artifact. Record what produced it:

```json
{
  "video_id": "EP012",
  "brief_hash": "sha256:…",
  "components": { "type.stat": "1.3.0", "motion.slam": "1.1.0", "end.card": "2.0.0" },
  "renderers": { "code": "remotion@4.0", "generative": "model-x@2026-11" },
  "palette_hash": "sha256:…",
  "output_hash": "sha256:…"
}
```

Then "style v3 performed better than v2" becomes a measurable claim rather than a memory. When a component is upgraded, you can re-render last month's winner to confirm the upgrade did not break it — which is impossible if you cannot reproduce builds.

Store it beside the output: `out/EP012.build.json`.

## Promotion and retirement

- A component used in 5+ videos is **core** — freeze its API, change only by version bump.
- A component used once is a **candidate** — keep it, do not build on it.
- A component whose videos underperform the page median twice is **retired** — move it to `archive/`, stop scheduling it.

Keeping a zombie library is as costly as having no library: the model picks from whatever is available, and it will pick the dead ones.

## What the model needs

Give the renderer the **component catalogue with parameter schemas**, not prose about the style. A model choosing from a typed catalogue stays on-brand. A model told "make it feel premium" invents something new and slightly wrong every time.

The catalogue is the brand. Everything else is decoration.
