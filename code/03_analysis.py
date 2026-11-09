"""Step 3: counts by word, county, town and 20 km hexagon; the meeting zones; results.json and the data tables."""
import pandas as pd, numpy as np
from common import *
from words import WORDS, WLAB, WKIND, WNOTE, REGIONAL

A = pd.read_csv(f"{DATA}/alleys.csv", dtype={"first_way": str, "ways": str}, keep_default_na=False)
A["path"] = A.path.astype(str).isin(["True", "true", "1"])
RV = jload(f"{WORK}/review.json")
W = pd.read_csv(f"{WORK}/ways.csv", dtype={"way": str}, keep_default_na=False)
R = {"n": {"ways_raw": int(len(W)), "candidates": RV["candidates"], "dropped": RV["dropped"], "dropped_by_hand": RV["dropped_by_hand"],
           "alleys": int(len(A)), "ways_in_alleys": int(A.n_ways.sum()), "regional": int(A.word.isin(REGIONAL).sum()),
           "general": int((~A.word.isin(REGIONAL)).sum()), "words_found": int(A.word.nunique())}}
R["n"]["dropped_pc"] = 100 * RV["dropped"] / RV["candidates"]
R["n"]["merged_ways"] = int(A.n_ways.sum() - len(A))

# ---- each word: where it lives
HOME = {"twitten": ["East Sussex", "West Sussex"], "loke": ["Norfolk", "Suffolk"], "chare": ["Tyne and Wear", "Durham", "Northumberland"],
        "ope": ["Devon", "Cornwall", "Dorset"], "shut": ["Shropshire"], "lonnen": ["Tyne and Wear", "Durham", "Northumberland", "Cumbria"],
        "jitty": ["Leicestershire", "Northamptonshire", "Rutland", "Lincolnshire", "Nottinghamshire", "Derbyshire", "Warwickshire", "West Midlands"],
        "twitchel": ["Nottinghamshire", "Derbyshire", "Lincolnshire", "South Yorkshire"],
        "ginnel": ["West Yorkshire", "Greater Manchester", "Lancashire", "South Yorkshire", "North Yorkshire", "Merseyside", "Cumbria", "Derbyshire"],
        "snicket": ["West Yorkshire", "North Yorkshire", "South Yorkshire", "East Riding of Yorkshire"],
        "drang": ["Somerset", "Devon", "Cornwall"]}
SCOT = {"wynd", "close", "vennel", "pend"}
words = {}
for k, lab, sp, col, kind, note in WORDS:
    s = A[A.word == k]
    if not len(s):
        continue
    cc = s.county.value_counts()
    tt = s[s.town != ""].town.value_counts()
    d = {"n": int(len(s)), "label": lab, "kind": kind, "path_pc": 100 * s.path.mean(), "top_county": cc.index[0], "top_county_n": int(cc.iloc[0]),
         "top_county_pc": 100 * cc.iloc[0] / len(s), "top_town": tt.index[0] if len(tt) else "", "top_town_n": int(tt.iloc[0]) if len(tt) else 0,
         "counties": int(s.county.nunique()), "scotland_pc": 100 * (s.nation == "Scotland").mean(), "lat": float(s.lat.mean()), "lon": float(s.lon.mean())}
    if k in HOME:
        d["home_pc"] = 100 * s.county.isin(HOME[k]).mean(); d["home_n"] = int(s.county.isin(HOME[k]).sum()); d["home"] = HOME[k]
    words[k] = d
R["words"] = words
R["sussex_twitten_n"] = int(A[(A.word == "twitten")].county.isin(HOME["twitten"]).sum())
R["norfolk_loke_pc"] = 100 * (A[A.word == "loke"].county == "Norfolk").mean()
R["scot_words_pc"] = {k: 100 * (A[A.word == k].nation == "Scotland").mean() for k in SCOT}
wy = A[A.word == "wynd"]
R["wynd"] = {"scotland_n": int((wy.nation == "Scotland").sum()), "ne_england_n": int(wy.county.isin(["Durham", "Tyne and Wear", "Northumberland", "North Yorkshire", "Cumbria"]).sum()),
             "path_pc": 100 * wy.path.mean(), "road_pc": 100 * (~wy.path).mean()}
# the Scottish old-town closes: Edinburgh
cl = A[A.word == "close"]
R["close"] = {"edinburgh_n": int((cl.county == "City of Edinburgh").sum()), "edinburgh_pc": 100 * (cl.county == "City of Edinburgh").mean()}
# ---- regional vs general by nation
R["nations"] = {}
for nat, s in A.groupby("nation"):
    R["nations"][nat] = {"n": int(len(s)), "regional_pc": 100 * s.word.isin(REGIONAL).mean()}
lon = A[A.county == "Greater London"]
R["london"] = {"n": int(len(lon)), "regional_n": int(lon.word.isin(REGIONAL).sum()), "general_pc": 100 * (~lon.word.isin(REGIONAL)).mean(),
               "passage_n": int((lon.word == "passage").sum()), "alley_n": int((lon.word == "alley").sum())}

# ---- towns
T = A[A.town != ""]
tc = T.groupby("town").agg(n=("id", "size"), regional=("word", lambda s: int(s.isin(REGIONAL).sum())), words=("word", "nunique"),
                           top=("word", lambda s: s.value_counts().index[0]), lon=("lon", "mean"), lat=("lat", "mean")).reset_index()
tc["top_regional"] = [(T[(T.town == t) & T.word.isin(REGIONAL)].word.value_counts().index[0] if r > 0 else "") for t, r in zip(tc.town, tc.regional)]
tc = tc.sort_values(["n", "regional"], ascending=False)
tc.round(5).to_csv(f"{DATA}/towns.csv", index=False)
R["towns_all"] = [{"town": r.town, "n": int(r.n), "top": r.top, "regional": int(r.regional), "words": int(r.words)} for r in tc.head(12).itertuples()]
tr = tc.sort_values(["regional", "n"], ascending=False)
R["towns_regional"] = [{"town": r.town, "regional": int(r.regional), "top": r.top_regional, "n": int(r.n)} for r in tr.head(12).itertuples()]
R["towns_most_words"] = [{"town": r.town, "words": int(r.words), "n": int(r.n)} for r in tc.sort_values(["words", "n"], ascending=False).head(6).itertuples()]
for k in ("chare", "ope", "shut", "loke", "twitten", "entry", "pend", "vennel", "close", "jitty", "ginnel", "snicket", "gully"):
    s = T[T.word == k].town.value_counts()
    R.setdefault("word_town", {})[k] = [{"town": t, "n": int(n)} for t, n in s.head(4).items()]

# ---- 20 km hexagons (pointy-top, 20 km across the flats) on the British National Grid
S = 20000 / math.sqrt(3)


def hexid(x, y):
    q = (math.sqrt(3) / 3 * x - y / 3) / S; r = (2 / 3 * y) / S
    cx, cz = q, r; cy = -cx - cz
    rx, ry, rz = round(cx), round(cy), round(cz)
    dx, dy, dz = abs(rx - cx), abs(ry - cy), abs(rz - cz)
    if dx > dy and dx > dz: rx = -ry - rz
    elif dy > dz: ry = -rx - rz
    else: rz = -rx - ry
    return int(rx), int(rz)


def hexcorners(q, r):
    cx = S * math.sqrt(3) * (q + r / 2); cy = S * 1.5 * r
    return [(cx + S * math.cos(math.radians(60 * i - 30)), cy + S * math.sin(math.radians(60 * i - 30))) for i in range(6)]


A["hq"], A["hr"] = zip(*[hexid(x, y) for x, y in zip(A.x, A.y)])
cells = []
from pyproj import Transformer
inv = Transformer.from_crs(27700, 4326, always_xy=True)
for (q, r), s in A.groupby(["hq", "hr"]):
    reg = s[s.word.isin(REGIONAL)]
    vc = reg.word.value_counts()
    top = vc.index[0] if len(vc) else ""
    tie = len(vc) > 1 and vc.iloc[0] == vc.iloc[1]
    cs = [inv.transform(x, y) for x, y in hexcorners(q, r)]
    cells.append({"q": q, "r": r, "n": int(len(s)), "regional": int(len(reg)), "top": top if not tie else "tie", "top_n": int(vc.iloc[0]) if len(vc) else 0,
                  "second": vc.index[1] if len(vc) > 1 else "", "second_n": int(vc.iloc[1]) if len(vc) > 1 else 0,
                  "general_top": s[~s.word.isin(REGIONAL)].word.value_counts().index[0] if (~s.word.isin(REGIONAL)).any() else "",
                  "words": "; ".join(f"{w} {n}" for w, n in s.word.value_counts().items()),
                  "corners": [[round(a, 4), round(b, 4)] for a, b in cs]})
C = pd.DataFrame(cells)
C.drop(columns=["corners"]).to_csv(f"{DATA}/hexagons.csv", index=False)
jsave({"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {k: c[k] for k in ("n", "regional", "top", "top_n", "second", "second_n", "words")},
       "geometry": {"type": "Polygon", "coordinates": [c["corners"] + [c["corners"][0]]]}} for c in cells]}, f"{DATA}/hexagons.geojson")
dom = C[(C.regional >= 3) & (C.top != "tie")]
R["hex"] = {"cells": int(len(C)), "cells_regional3": int((C.regional >= 3).sum()), "ties": int(((C.regional >= 3) & (C.top == "tie")).sum()),
            "dominant": dom.top.value_counts().to_dict()}
# meeting zones: hexagons where two regional words both have at least two alleys
mix = C[(C.second_n >= 2)].sort_values("regional", ascending=False)
R["mixed_cells"] = [{"words": r.words, "n": int(r.n)} for r in mix.head(8).itertuples()]
# ginnel against snicket in Yorkshire
Y = A[A.county.isin(["West Yorkshire", "North Yorkshire", "South Yorkshire", "East Riding of Yorkshire"]) & A.word.isin(["ginnel", "snicket"])]
R["yorks"] = {"ginnel": int((Y.word == "ginnel").sum()), "snicket": int((Y.word == "snicket").sum()),
              "ginnel_towns": sorted(set(Y[Y.word == "ginnel"].town) - {""}), "snicket_towns": sorted(set(Y[Y.word == "snicket"].town) - {""})}
wh = A[A.word.isin(["ginnel", "snicket"]) & (A.lat > 53.85) & (A.lat < 53.95) & (A.lon > -1.8) & (A.lon < -1.5)]
R["wharfedale"] = {"snicket": int((wh.word == "snicket").sum()), "ginnel": int((wh.word == "ginnel").sum())}
sn, gi = wh[wh.word == "snicket"], A[A.word == "ginnel"]
d = km(sn.lat.values[:, None], sn.lon.values[:, None], gi.lat.values[None, :], gi.lon.values[None, :])
R["wharfedale"]["min_km"] = float(d.min())
R["wharfedale"]["nearest_ginnel_town"] = gi.town.values[d.min(0).argmin()]
R["york"] = {"snicket": int(((A.word == "snicket") & (A.town == "York")).sum()), "ginnel": int(((A.word == "ginnel") & (A.town == "York")).sum()),
             "all": int((A.town == "York").sum())}
# by county table
bc = A.pivot_table(index="county", columns="word", values="id", aggfunc="size", fill_value=0)
bc["total"] = bc.sum(axis=1)
bc.sort_values("total", ascending=False).to_csv(f"{DATA}/by_county.csv")
R["counties_with_regional"] = int((bc[[c for c in bc.columns if c in REGIONAL]].sum(axis=1) > 0).sum())
R["counties"] = int(len(bc))
jsave(R, f"{DATA}/results.json", indent=1)
print(json.dumps({k: R[k] for k in ("n", "hex", "yorks", "wharfedale", "york", "london", "close", "wynd", "nations")}, indent=0, default=str)[:3000])
for k, v in words.items():
    print(k, v["n"], v["top_county"], round(v["top_county_pc"]), v.get("home_pc"), v["top_town"], v["top_town_n"], round(v["path_pc"]))
print(R["towns_all"][:8]); print(R["towns_regional"][:8]); print(R["mixed_cells"])
