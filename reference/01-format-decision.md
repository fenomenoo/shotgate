# 01 — Choosing the format

The format comes from the **audience**, not from what your tools can render. This is the most common failure point: people pick the style that looks impressive in a demo, then post a random mix and nothing sticks.

## Answer three questions in writing

Write the answers down. A format chosen in your head is a format you will abandon in week three.

**1. What does this person already watch, before they know they need us?**

Not "what do our customers like" — what is in their feed *already*. If the audience watches true-crime longform and you post flat 2D explainers, you are competing for a slot you do not hold. Meet the behaviour that exists.

**2. Does the product have to be seen working, or understood?**

- Seen working → screen capture, product demos, before/after. The product is the hero.
- Understood → explainer, motion graphics, diagrams. The *idea* is the hero, the product appears at the end.

Most apps answer this wrong. A finance tracker does not need to be seen working for 20 seconds; it needs the problem understood in 8.

**3. Who has to trust it — someone scrolling at 11pm, or a buyer evaluating at work?**

- 11pm scroller → pace, colour, sound, momentum. Emotion and rhythm over precision.
- Buyer at work → clarity, sources, no gimmicks, sound-off readability. Precision over rhythm.

These produce different videos for the same product. Pick one per page and do not blend.

## Matching table

| Product type | Format | Substrate | Recurring element |
|---|---|---|---|
| Consumer (pets, fitness, hobbies, language) | 3D cutaway / cartoon cast / painted story | generative + code hybrid | a character with a name |
| Understood-not-seen (finance, health tracking, dev tools) | explainer, one question per video | code render (HTML/three.js/Remotion) | a diagram motif |
| Story behind the problem | archival / documentary | archival footage + code typography | a real event |
| Launch or big moment | cinematic | generative video | none — use rarely |
| Utility, lists, stats, history | motion typography / data-viz | code render | a fixed grid or palette |
| Physical product or SaaS workflow | screen capture + callouts | screen recording + code overlay | the cursor |

## Rules

1. **One main format per page**, plus exactly one format under test.
2. **A new style gets a new page** or its own numbered series. Never mix two styles on one page — the audience follows a pattern, not a brand.
3. **Five videos before judging a format.** One video tells you nothing; five tells you whether the format or the execution failed.
4. **When a video hits, keep the style and the hook shape.** Change the subject tomorrow. Do not change the format because it worked.

## Decision record

Append one row per page to `data/format-decisions.csv`:

```csv
page,date,q1_watching,q2_seen_or_understood,q3_trust_context,chosen_format,test_format,substrate
```

This is how you stop re-litigating the format every Monday, and how you notice when a page has drifted into a mix.

## The failure mode to watch for

A page starts with one format, gets bored, adds a second because a competitor's video did well, then a third because a trend appeared. Three months later it is a random mix with no retention signal and no way to tell what worked. The rule exists to prevent exactly this.
