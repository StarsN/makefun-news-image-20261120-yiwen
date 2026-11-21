# The World in One Image — Friday 20 November 2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/StarsN/makefun-news-image-20261120-yiwen/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/StarsN/makefun-news-image-20261120-yiwen/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A newspaper front page that sums up Friday 20 November 2026 in a single
1024×1024 image, built for the
[make.fun news-image-20261120 bounty](https://make.fun/bounty/news-image-20261120).

## What the day held

- **Shenzhen summit** — Trump, Xi and Putin hold their first three-way
  meeting and sign a four-point joint peace declaration.
- **The Hague** — the International Court of Justice rules Myanmar
  committed genocide against the Rohingya, a first against a state.
- **Kyiv** — eight killed as overnight Russian strikes hit bridges over
  the Dnipro; Poland reports its airspace breached.
- **Riyadh** — a Houthi missile damages the PIF tower in the capital's
  financial district.
- **Markets** — the Nikkei falls 4.8% and the S&P 500 slides for a fifth
  straight session on doubts over AI valuations.
- **Cyclone Akvan** — 300,000 people evacuated as the storm makes
  landfall on India's Odisha coast.

## How it is made

`compose.py` (Python 3 + Pillow) lays out the front page from three
illustrations generated for this entry — the Shenzhen signing, Kyiv
under attack, and the Riyadh tower — and writes `entry.png`. `main.ts`
(Node 22, standard library only) copies that image, byte for byte, to
`$MAKEFUN_OUTPUT_DIR/entry.png`.

## Run it

```sh
python3 compose.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Both runs of `main.ts` write the same bytes. The program uses no
network.

## License

MIT — see [LICENSE](LICENSE).
