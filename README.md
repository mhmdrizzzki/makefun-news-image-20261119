# One page for Thursday 19 November 2026

[![make.fun bounty](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/mhmdrizzzki/makefun-news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/mhmdrizzzki/makefun-news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119)

An entry for make.fun's [Sum up 19 November's world news in one image](https://make.fun/bounty/news-image-20261119).

A single front page for that Thursday, built as a real one:

- **47 stories** first reported on 19 November 2026, every one carrying its UTC time
- a navy masthead with the date, a stamped **NOV 19 2026**, and a **five-slot UTC timeline**
- **one dominant hero** (the three-way summit in Shenzhen), two stacked side leads
  (the record Anthropic listing, Cyclone Akvan), and seven pictogram cards
- a world map whose numbered pins follow stories 1–10, colour-coded by region
- **33 briefs** in three balanced columns, from every continent
- a red **DATE CHECK** box listing four stories that broke on 18 November and are
  therefore deliberately kept off the page

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Standard library only, no network, deterministic: both runs write the same bytes.

`main.py` validates the image before shipping it — the 1 MiB cap, the PNG
signature, a 13-byte IHDR with dimensions ≤ 1024 and bit depth 8, a permitted
colour type, exactly one IHDR first, a chunk walk to an empty IEND and no bytes
after it — and writes nothing at all when a check fails.

## Files

- `main.py` — the entry program
- `entry.png` — the image it ships (1024×1024, byte-identical to `entry_v2.png`)
- `test_main.py` — regression tests: good image passes, truncated refused, over-size refused

```sh
python3 -m unittest -v test_main
```

Licensed MIT.
