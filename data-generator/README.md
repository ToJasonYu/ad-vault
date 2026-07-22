# data-generator

Fabricates a synthetic ad ecosystem: advertisers, campaigns, users, and impression/click
events. Click behavior isn't random — users have an interest segment, campaigns have a
category, and matching the two boosts click probability. That gives the ML service (Day 2)
a real, if modest, pattern to learn instead of pure noise.

## Usage

```
python generate_data.py
```

Writes `advertisers.csv`, `campaigns.csv`, `users.csv`, and `events.csv` to `./output/` by
default. Run with `--seed 42` (the default) to get the same data every time, or override any
of `--n-advertisers`, `--campaigns-per-advertiser`, `--n-users`, `--n-events`, `--output-dir`.

Output isn't committed to the repo — it's regenerated deterministically from the script, so
there's nothing to keep in sync.
