"""Brier score and a 10-bin calibration table for the model's pick probability.

    python examples/brier.py            # live file
    python examples/brier.py data/all.csv
"""
import sys
import pandas as pd

src = sys.argv[1] if len(sys.argv) > 1 else "https://footballanalytics.pro/data/all.csv"
df = pd.read_csv(src)

for k, col in (("1", "p_home"), ("X", "p_draw"), ("2", "p_away")):
    df[f"sq_{k}"] = ((df.result == k).astype(float) - df[col]) ** 2
df["brier"] = df[["sq_1", "sq_X", "sq_2"]].sum(axis=1)
print("matches:", len(df))
print(df.groupby("league")[["brier", "pick_correct"]].agg(["mean", "count"]).round(3))

picked = df.dropna(subset=["pick"]).copy()
picked["p_pick"] = picked.apply(lambda r: r[{"1": "p_home", "X": "p_draw", "2": "p_away"}[r.pick]], axis=1)
picked["bin"] = pd.cut(picked.p_pick, bins=[0, .35, .4, .45, .5, .55, .6, .65, .7, .8, 1.0])
cal = picked.groupby("bin", observed=True).agg(n=("pick_correct", "size"), predicted=("p_pick", "mean"), observed=("pick_correct", "mean")).round(3)
print("\ncalibration of the pick probability:\n", cal)
