"""Step 2: false friends out, by rule and by hand (code/overrides.csv), after reading every alley of the ambiguous words
(WORK/review_*.txt). Rules:
- jetty counts as a jitty only in the East Midlands and next door (Leicestershire, Northamptonshire, Rutland, Lincolnshire,
  Nottinghamshire, Derbyshire, Warwickshire, West Midlands); elsewhere a jetty is a pier or landing stage.
- cut counts only on footpath-type ways (footway, pedestrian, path, steps), never 'New Cut' (a canal, drain or new road)
  or a cycle trail (old railway cuttings), and never when any piece of it is a road (The Cut in Southwark is a street);
  everything else named Cut is a road or a waterway.
- steps on a countryside path, track or bridleway more than 3 km from a place of 3,000 people are hill paths, not town steps.
- close counts only for footpaths in Scotland (in England a Close is usually a cul-de-sac); made in step 1.
Writes data/alleys.csv and WORK/dropped.csv."""
import pandas as pd, numpy as np
from scipy.spatial import cKDTree
from common import *
from words import WORDS, PATH_TYPES

G = pd.read_csv(f"{WORK}/alleys_raw.csv", dtype={"ways": str})
O = pd.read_csv(os.path.join(ROOT, "code", "overrides.csv"))   # optional lat, lon: only the alley within 1 km of that point
EM = {"Leicestershire", "Northamptonshire", "Rutland", "Lincolnshire", "Nottinghamshire", "Derbyshire", "Warwickshire", "West Midlands"}
first_hw = G.hws.str.split(";")
G["why"] = ""
spelt = G.name.str.lower()
m = (G.word == "jitty") & spelt.str.contains(r"\bjetty\b") & ~G.county.isin(EM)
G.loc[m, "why"] = "jetty: a pier or landing stage outside the East Midlands"
ROADS = {"residential", "unclassified", "tertiary", "secondary", "primary", "trunk", "tertiary_link", "secondary_link", "primary_link", "trunk_link"}
pathlike = first_hw.apply(lambda s: bool(set(s) & {"footway", "pedestrian", "path", "steps"}) and not set(s) & ({"cycleway", "track"} | ROADS))
m = (G.word == "cut") & (~pathlike | spelt.str.contains(r"\bnew cut\b"))
G.loc[m & (G.why == ""), "why"] = "cut: a road, waterway or cycle trail"
T = settlements(3000)
tx, ty = bng(T.lon.values, T.lat.values)
d, i = cKDTree(np.c_[tx, ty]).query(G[["x", "y"]].values)
G["near_km"] = d / 1000
countryside = first_hw.apply(lambda s: set(s) <= {"path", "track", "bridleway", "footway", "steps"} and bool(set(s) & {"path", "track", "bridleway"}))
m = (G.word == "steps") & countryside & (G.near_km > 3)
G.loc[m & (G.why == ""), "why"] = "steps: a hill path in the countryside"
for o in O.itertuples():
    m = (G.word == o.word) & (G.name == o.name) & (G.county == o.county)
    if o.lat == o.lat:
        m &= km(G.lat.values, G.lon.values, o.lat, o.lon) < 1
    assert m.any(), o
    G.loc[m, "why"] = f"{o.word}: {o.reason} (by hand)"
D = G[G.why != ""]
D.to_csv(f"{WORK}/dropped.csv", index=False)
A = G[G.why == ""].drop(columns=["why"]).copy()
print("dropped", len(D), D.why.str.split(":").str[0].value_counts().to_dict())
for w in ("steps",):
    print(D[D.word == w][["name", "county", "near_km"]].to_string()[:3000])
# nearest town of 10,000 people or more within 6 km (else none)
T10 = settlements(10000)
tx, ty = bng(T10.lon.values, T10.lat.values)
d, i = cKDTree(np.c_[tx, ty]).query(A[["x", "y"]].values)
A["town"] = np.where(d <= 6000, T10.name.values[i], "")
A["town_qid"] = np.where(d <= 6000, T10.qid.values[i], "")
A.loc[A.county == "Greater London", "town"] = "London"           # Wikidata types some London districts (Stepney, Fulham) as towns
A.loc[A.county == "Greater London", "town_qid"] = "Q84"
A["first_way"] = A.ways.str.split(";").str[0]
A = A.sort_values(["word", "county", "name"]).reset_index(drop=True)
A["id"] = np.arange(len(A))
A[["id", "word", "name", "lon", "lat", "x", "y", "county", "nation", "town", "town_qid", "n_ways", "hws", "path", "first_way", "ways"]].round(
    {"lon": 5, "lat": 5, "x": 0, "y": 0}).to_csv(f"{DATA}/alleys.csv", index=False)
print("alleys", len(A)); print(A.word.value_counts().to_string())
jsave({"dropped": int(len(D)), "dropped_by_word": D.word.value_counts().to_dict(), "dropped_by_hand": int(D.why.str.contains("by hand").sum()),
       "candidates": int(len(G))}, f"{WORK}/review.json")
