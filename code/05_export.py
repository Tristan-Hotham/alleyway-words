"""Step 5: page data. data/alleys.json (every alley, compact rows), data/places.json (towns of 5,000 people or more, for the
search); data/hexagons.geojson is written by step 3."""
import pandas as pd
from common import *
from words import WORDS

A = pd.read_csv(f"{DATA}/alleys.csv", keep_default_na=False, dtype={"first_way": str})
WI = {w[0]: i for i, w in enumerate(WORDS)}
cnt = A.word.value_counts()
rows = [[round(r.lon, 5), round(r.lat, 5), WI[r.word], r.name, r.county, r.town, int(r.first_way), int(r.n_ways), 1 if str(r.path) == "True" else 0,
         r.hws.replace(";", ", ")] for r in A.itertuples()]
jsave({"words": [[k, lab, col, kind, note, int(cnt.get(k, 0))] for k, lab, sp, col, kind, note in WORDS], "rows": rows}, f"{DATA}/alleys.json")
T = settlements(5000)
jsave({"places": [[r.name, round(r.lon, 4), round(r.lat, 4)] for r in T.sort_values("pop", ascending=False).itertuples()]}, f"{DATA}/places.json")
print("alleys.json", os.path.getsize(f"{DATA}/alleys.json") // 1024, "KB; places", len(T))
