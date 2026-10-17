# footballanalytics.pro — open data

Settled football match predictions of the [Football Analytics](https://footballanalytics.pro) model: for every finished match in 11 covered leagues, the 1X2 probabilities and goal expectations the model stored **before kick-off**, its pick, and the final score. Nothing is filtered by outcome — losing picks sit next to winning ones.

- Documentation and column reference: <https://footballanalytics.pro/en/data>
- Live files (refreshed hourly): `https://footballanalytics.pro/data/all.csv` · `https://footballanalytics.pro/data/{league-slug}.csv` · `.json` variants
- Track record with calibration and closing-line ROI: <https://footballanalytics.pro/en/performance>
- Method (Dixon-Coles / Poisson with ELO prior): <https://footballanalytics.pro/en/methodology>

This repository mirrors the files once a day (`data/`) so a season can be cited at a fixed commit.

## Files

| File | Content |
|---|---|
| `data/all.csv` | every settled match, all leagues |
| `data/<league-slug>.csv` | one league (`premier-league`, `championship`, `la-liga`, `serie-a`, `bundesliga`, `ligue-1`, `eredivisie`, `liga-portugal`, `champions-league`, `brasileirao`, `super-lig`) |

One row per match, UTF-8, comma-separated, kick-off order. Columns:

`fixture_id, kickoff_utc, league, league_slug, country, home_team, away_team, home_score, away_score, result, p_home, p_draw, p_away, lambda_home, lambda_away, pick, pick_correct, model_version, match_url`

`result` is 1 / X / 2 from the score; `pick` is the model's pre-match argmax; `pick_correct` is 1/0 (empty without a pick); `lambda_*` are the model's Poisson goal rates (not shot-based xG).

## Quick start

```python
import pandas as pd
df = pd.read_csv("https://footballanalytics.pro/data/all.csv")
df["brier"] = ((df.result == "1") - df.p_home) ** 2 + ((df.result == "X") - df.p_draw) ** 2 + ((df.result == "2") - df.p_away) ** 2
print(df.groupby("league")[["brier", "pick_correct"]].mean().round(3))
```

See `examples/brier.py` for a calibration table.

## What the data is, and is not

- Pre-match figures only: written before kick-off, never revised.
- Settled matches only: a fixture appears once it has a final score. Upcoming predictions are not published.
- Covered leagues only; the model is fitted per league.
- No bookmaker odds (third-party data, not redistributed).
- Data starts June 2026, when the current model went live.

## Licence

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Use it for anything, including commercial work; credit **Football Analytics** and link to <https://footballanalytics.pro/data>.

Suggested citation:

> Football Analytics (2026). Settled model predictions dataset: pre-match 1X2 probabilities and results, 11 leagues. https://footballanalytics.pro/data. Licence: CC BY 4.0.
