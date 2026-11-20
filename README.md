# Thursday 19 November 2026: 46 stories, 6 continents, one front page (v3 final)

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/haidildariell/news-image-20261119-v3/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/haidildariell/news-image-20261119-v3/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One image that sums up **Thursday 19 November 2026** — a newspaper front page
with **46 verified stories from 6 continents**: the first-ever Trump–Xi–Putin
three-way summit in Shenzhen, GTA VI going on sale worldwide (Metacritic 99),
and Anthropic's record $81.3bn IPO debut on Nasdaq (ANT: opened $111.50,
closed $97.17, +17%).

## What's inside

- **Masthead** — giant date, red subhead with the 3 top stories, region strip
  (ASIA 11 · EUROPE 13 · MIDDLE EAST 5 · AMERICAS 6 · OCEANIA 5 · AFRICA 4 ·
  GLOBAL 2 = 46), big-number stat strip.
- **3 illustrated leads** — APEC summit, GTA VI, Anthropic (flat art drawn
  from Pillow primitives, no external assets).
- **12 mid cards** with small icons — ICJ genocide ruling (9–6), COP31 draft,
  Cyclone Akvan, the Suneung exam, Australia's 4.9% jobless rate, the Crimea
  bridge, Riyadh, the Arctic pact (109–0), Bangladesh, the Senate Iran vote,
  Colombia's strike, Indonesia's asset-seizure law.
- **Dot-matrix world map** — 46 stories pinned and numbered, plus THE VERDICT
  (ICJ 9–6).
- **31 numbered one-liners**, a THE DAY BY HOURS timeline, a DATE CHECK box
  listing 18 November (or earlier) news that was explicitly *excluded*, and a
  sources footer.

## Honesty

Every story happened, or was first reported, on Thursday 19 November 2026
(in any time zone), and each is backed by at least two sources (see
[SOURCES.md](SOURCES.md)). Claims are attributed, not stated as fact — items
that rest on one side's claim are tagged **CLAIM**, projections **FORECAST**.

## Build & run

```bash
python3 build_image.py   # writes entry.png (1024x1024, deterministic)
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py   # copies entry.png to $MAKEFUN_OUTPUT_DIR/entry.png
```

Requirements: Python 3 + Pillow. No network at build/run time; all facts are
hardcoded in `build_image.py` from the verified recon blueprint.

## License

MIT — see [LICENSE](LICENSE).
