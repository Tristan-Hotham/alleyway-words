"""Step 1: OSM ways -> classified alley names -> merged alleys.
Reads STREETS; writes WORK/ways.csv (every way with its head word) and WORK/alleys.csv (ways of one name within 150 m
merged into one alley), plus WORK/review_*.txt, the full lists read by eye for the false-friend checks."""
import pandas as pd, numpy as np
import geopandas as gpd
from common import *
from words import WMAP, PATH_TYPES

rows = []
for r in read_tsv(STREETS):
    lon, lat = point(r["p"])
    if lon is None or not r["name"]:
        continue
    rows.append({"way": r["w"].rsplit("/", 1)[-1], "hw": r["hw"], "name": r["name"].strip(), "lon": lon, "lat": lat})
W = pd.DataFrame(rows)
print("ways", len(W))


def head(name):
    """the head word of a name and the cleaned name it came from"""
    s = re.sub(r"\(.*?\)", " ", name)                       # 'The Snicket (CSB20)'
    s = re.split(r"\s[-–]\s|:\s", s)[0]                    # 'Twitten - Vernon Avenue to McWilliam Road'
    s = re.sub(r"\b(no\.?\s*)?\d+[a-z]?\b\.?$", " ", s.strip(), flags=re.I)   # 'Ginnel No 7', 'Solar Rise Ginnel 1'
    s = re.sub(r"[.,;]+$", "", s.strip())
    toks = re.findall(r"[A-Za-z']+", s)
    if not toks:
        return "", s
    return toks[-1].lower().replace("'", ""), s


x, y = bng(W.lon.values, W.lat.values)
W["x"], W["y"] = x, y
# counties (ONS) for every way
C = gpd.read_file(f"{GEO}/counties_uk.geojson").to_crs(27700)
P = gpd.GeoDataFrame(W[["way"]], geometry=gpd.points_from_xy(W.x, W.y), crs=27700)
J = gpd.sjoin_nearest(P, C[["county", "nation", "geometry"]], how="left", max_distance=3000)
J = J[~J.index.duplicated()]
W["county"], W["nation"] = J["county"].values, J["nation"].values
# misspellings and duplicate ways of one alley, found when reading the lists (code/renames.csv)
RN = pd.read_csv(os.path.join(ROOT, "code", "renames.csv"))
for o in RN.itertuples():
    m = (W.name == o.name) & (W.county == o.county)
    assert m.sum() >= 1, o
    W.loc[m, "name"] = o.new_name
W[["head", "clean"]] = W.name.apply(lambda n: pd.Series(head(n)))
W["word"] = W["head"].map(WMAP)
W["path"] = W.hw.isin(PATH_TYPES)
W.to_csv(f"{WORK}/ways.csv", index=False)
print("ways with an alley head word", W.word.notna().sum())
print(W[W.word.notna()].word.value_counts().to_string())

# the candidate alleys: head word in the list, plus the Scottish footpath 'close'
A = W[W.word.notna()].copy()
A = A[(A.word != "close") | ((A.nation == "Scotland") & A.path)]
A["norm"] = A.clean.str.lower().str.replace(r"[^a-z ]", "", regex=True).str.replace(r"^the ", "", regex=True).str.replace(r"\bsaint\b", "st", regex=True).str.split().str.join(" ")
A["gid"] = merge_close(A, 150)
# a street or a named path is often mapped in pieces longer than 150 m: join pieces of one name that chain within 600 m when
# the alley includes a road-type way or the name has a specific element ('Cornish Snicket'); bare names ('Snicket',
# 'The Wynd') on footpaths keep the 150 m rule, since several separate paths can carry the same bare name
bare = A.norm.str.split().str.len() == 1
long_ = (A.groupby("gid").path.transform("min") == 0) | ~bare
R_ = A[long_].copy(); R_["gid2"] = merge_close(R_, 600)
first = R_.groupby("gid2").gid.transform("min")
A.loc[long_, "gid"] = first.values
G = A.groupby("gid").agg(name=("name", lambda s: s.value_counts().index[0]), norm=("norm", "first"), word=("word", "first"),
                         lon=("lon", "mean"), lat=("lat", "mean"), x=("x", "mean"), y=("y", "mean"), n_ways=("way", "size"),
                         ways=("way", lambda s: ";".join(s)), hws=("hw", lambda s: ";".join(sorted(set(s)))), path=("path", "max"),
                         county=("county", "first"), nation=("nation", "first")).reset_index(drop=True)
G.to_csv(f"{WORK}/alleys_raw.csv", index=False)
print("alleys before review", len(G))
# lists for the by-eye review of every case of the ambiguous words
T = settlements(3000)
from scipy.spatial import cKDTree
tx, ty = bng(T.lon.values, T.lat.values)
d, i = cKDTree(np.c_[tx, ty]).query(G[["x", "y"]].values)
G["near"] = T.name.values[i]; G["near_km"] = (d / 1000).round(1)
for w in sorted(G.word.unique()):
    with open(f"{WORK}/review_{w}.txt", "w") as f:
        for r in G[G.word == w].sort_values(["county", "name"]).itertuples():
            f.write(f"{r.ways.split(';')[0]}\t{r.name}\t{r.hws}\t{r.county}\t{r.near} {r.near_km} km\t{r.lat:.4f},{r.lon:.4f}\n")
