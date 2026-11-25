# 08 — Attribution

Views do not pay. Installs do. And you cannot optimise what you cannot attribute — which is why the most common setup (one link per page) is also the most common reason people scale the wrong format for six months.

## The upgrade that matters

**One link per video, not per page.**

| Setup | What you learn |
|---|---|
| One link per page | whether the page works — nothing about which video did it |
| One link per video | which video, which hook, which style produced the install |

Per-video links cost nothing extra. Use a short-link service, a redirect endpoint, or a UTM parameter that varies per video — any of them works; having it is the point.

```
https://go.brand.com/v/EP012         → redirects to store/landing, logs the click
https://brand.com/app?utm_source=tiktok&utm_medium=video&utm_campaign=EP012&utm_content=hook_07
```

For app installs, use the store's own campaign links (App Store campaign links, Google Play referrer) so the video id survives the install. For SaaS, UTM plus one question at signup: **"where did you find us?"** — self-reported attribution covers what links miss.

## The chain

Track all five steps per format, weekly:

```
views → profile visits → link clicks → installs → paid
```

Each step has its own conversion rate, and each failure looks different:

| Where it breaks | What it means | What to change |
|---|---|---|
| views low | hook or format does not match the feed | hook family, format |
| views high, profile visits low | video entertains but does not sell a next step | end card, CTA, the promise in the hook |
| profile visits high, clicks low | bio does not continue the promise | bio copy, pinned video, link label |
| clicks high, installs low | landing or store page fails | landing copy, store screenshots, price |
| installs high, paid low | onboarding or product | not a content problem |

Most people diagnose a top-of-funnel problem as a bottom-of-funnel one. The chain tells you which link is actually broken.

## What to log

Per video, in `templates/video-log.csv`:

```csv
video_id,page,date,format,style,hook_pattern,hook_text,substrate,views,ret_3s_pct,shares,saves,profile_visits,link_clicks,installs,cost_usd
```

This single table is what makes every other file in this repo useful. Without it, the retention loop and the cost rollup have nothing to read.

## Reading it without fooling yourself

1. **Never compare a video to another page's video.** Different audiences, different baselines. Compare within a page, over time.
2. **Never rank by views.** Rank by installs per 1k views. A 12k-view video with 4 installs beats a 90k-view video with 1.
3. **Wait 14 days** before judging a video's installs. App-install attribution lags; day-1 numbers are noise.
4. **Cut on the two-week window, not the single video.** A format needs ~20 videos before its click-through rate is a signal rather than a coin flip.

## The one rule

If a format gets views but no clicks after twenty videos, cut it. The views are vanity and the audience is not your audience. This is the hardest rule to follow because the view count is the number you can see every day and installs are the number you can see every two weeks.
