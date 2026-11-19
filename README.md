# One page for Thursday 19 November 2026

[![make.fun bounty](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/mhmdrizzzki/makefun-news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/mhmdrizzzki/makefun-news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119)

An entry for make.fun's [Sum up 19 November's world news in one image](https://make.fun/bounty/news-image-20261119).

The image is a single front page for that Thursday: 42 stories first reported on
19 November 2026, three of them led with a drawing, six more in a grid, and
another thirty-three as briefs — with a world map whose numbered pins follow the
stories, and a **date check** box listing four stories that broke on 18 November
and are therefore deliberately kept off the page.

Twelve regions and beats are covered: a three-way summit in Shenzhen, the largest
listing on record, a cyclone emptying a coastline, a bridge struck again, a record
auction, a UN survey, the IEA's warning on datacentres, and the day's smaller
items from every continent.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Standard library only, no network, deterministic: both runs write the same bytes.

`main.py` validates `entry.png` before shipping it — PNG signature, IHDR
dimensions and bit depth, a complete chunk walk to `IEND`, and the 1 MiB cap —
and writes nothing at all when a check fails.

## Files

- `main.py` — the entry program
- `entry.png` — the image it ships (1024×1024)

Licensed MIT.
