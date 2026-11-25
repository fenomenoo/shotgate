# 04 — The hook factory

The first 1.5 seconds decide the video. Everything after it is a retention problem that a good hook has already half-solved.

Treat the hook as a **separate, swappable component** — not as the opening of a script. Because rendering is deterministic, you can render one video body with three different hooks almost for free and test which one holds. Almost nobody does this and it is the single cheapest advantage in the format.

## Rules

1. The hook must be **complete** by 1.5s — the promise, the tension or the question fully stated.
2. The hook must work **with the sound off**.
3. The hook must be **specific**. "This changed my life" is not a hook; "I cut my grocery bill by 40% in six weeks" is.
4. **One hook per video.** Two hooks are zero hooks.
5. **Name the pattern** in the brief and the log. An unnamed hook cannot be measured.

## 40 patterns

### Curiosity gap
1. **Withheld object** — something is almost revealed, cut before the reveal
2. **Number tease** — "three things", only two shown until the end
3. **Missing piece** — a diagram with one blank node
4. **Question without context** — the question lands before the subject does
5. **The wrong answer** — state a common belief, then contradict it
6. **Sealed box** — a covered or blanked element the viewer wants opened
7. **Countdown** — "by the end of this video…"

### Contradiction
8. **Everyone is wrong** — "everyone says X. X is backwards."
9. **Myth correction** — a specific myth, then the correction
10. **Expert disagrees** — quote an authority, then undercut it
11. **Opposite of expectation** — the counterintuitive claim first
12. **Fake rule** — state a rule the audience believes, then break it

### Number and scale
13. **Big number** — the largest figure on screen first
14. **Small number** — a tiny figure made to feel huge
15. **Ratio reveal** — "1 in 12"
16. **Cost per day** — big cost expressed per day
17. **Comparison stack** — two numbers side by side, one absurd
18. **Ladder** — 1 → 10 → 100 → 1000 in two seconds
19. **Zero** — "zero of these…"

### Personal stake
20. **POV** — first-person framing, second-person address
21. **Cost of inaction** — what it costs you to not know this
22. **Time wasted** — "you've been doing this for years"
23. **Direct callout** — "if you're a [specific person], stop scrolling"
24. **Confession** — "I was wrong about this"
25. **Loss framing** — the thing already lost

### Demonstration
26. **Mid-action open** — start at the most interesting frame of the video
27. **Result first** — show the outcome, then rewind
28. **Before/after snap** — half a second each
29. **Speed run** — the whole process accelerated
30. **Failure first** — show it going wrong, then the fix

### Structure
31. **List promise** — "five things, the last one matters"
32. **Timeline** — "in 1994, then in 2004, then everything changed"
33. **Two paths** — same starting point, two outcomes
34. **Rule break** — "nobody will tell you this, so I will"
35. **Chapter card** — a numbered, branded cold open
36. **Recurring catchphrase** — the same opening line every episode

### Visual
37. **Motion slam** — an object flies in and stops hard
38. **Scale jump** — extreme close-up to extreme wide in one cut
39. **Colour snap** — the palette inverts for a beat
40. **Text-first** — the hook is a full-screen line of type, no image

## Testing hooks

Render the same body with three hooks from different families (one curiosity, one number, one contradiction). Post across the page's slots over a week. Compare **retention at 3s**, not views.

Keep a hook log in `data/hooks.csv`:

```csv
video_id,hook_pattern,hook_text,ret_3s_pct,views,link_clicks
```

After 20 videos, sort by mean `ret_3s_pct` per pattern. You will find that 3–4 patterns carry your page. Write those first, always, and test one new family per month.

## The rule people break

They write a great hook, then bury it under a logo animation and a two-second establishing shot. The hook is frame one. There is no intro. Ever.
