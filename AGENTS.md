# Entry: one page for 19 November 2026

This repository is an entry for make.fun's `news-image-20261119` competition.

- `main.py` — the entry program (Python 3.13, standard library only, no network).
  It validates `entry.png` and copies it to `/output/entry.png`
  (or to `$MAKEFUN_OUTPUT_DIR` when that is set).
- `entry_v2.png` — the shipped image: one page summarising the world news first
  reported on Thursday 19 November 2026. `entry.png` is a byte-for-byte copy of
  it, kept under the name the program reads.
- `test_main.py` — regression tests for the validators in `main.py`
  (standard library only). Run them with:

      python3 -m unittest -v test_main

Run it locally:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

It must be deterministic: both runs write the same bytes.
