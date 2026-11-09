"""Step 4: figures for the page (img/*.jpg), the blog (release/blog/b_*.png, 1800 px) and the paper (release/paper/f_*.png)."""
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import matplotlib.patheffects as pe
from matplotlib.patches import Polygon as MP
from PIL import Image
from figstyle import *
from words import WORDS, WCOL, WLAB, REGIONAL, WKIND

R = jload(f"{DATA}/results.json")
A = pd.read_csv(f"{DATA}/alleys.csv", keep_default_na=False)
H = jload(f"{DATA}/hexagons.geojson")["features"]
TW = pd.read_csv(f"{DATA}/towns.csv", keep_default_na=False)
BLOG, PAPERD = f"{ROOT}/release/blog", f"{ROOT}/release/paper"
for d in (BLOG, PAPERD):
    os.makedirs(d, exist_ok=True)
CRS = 27700
EXT = (-8.3, 1.9, 49.9, 59.0)
HALO = [pe.withStroke(linewidth=3, foreground=PAPER)]
f27 = projector(CRS)
A["X"], A["Y"] = f27(A.lon.values, A.lat.values)


def out(fig, name, dpi=200):
    fig.savefig(f"{WORK}/{name}.png", dpi=dpi, facecolor=fig.get_facecolor())
    plt.close(fig)
    im = Image.open(f"{WORK}/{name}.png").convert("RGB")
    im.resize((1600, round(im.size[1] * 1600 / im.size[0])), Image.LANCZOS).save(f"{IMG}/{name}.jpg", quality=84, optimize=True)
    im.resize((1800, round(im.size[1] * 1800 / im.size[0])), Image.LANCZOS).save(f"{BLOG}/b_{name}.png", optimize=True)
    w = min(2000, im.size[0]); im.resize((w, round(im.size[1] * w / im.size[0])), Image.LANCZOS).save(f"{PAPERD}/f_{name}.png", optimize=True)
    os.remove(f"{WORK}/{name}.png")


def base(ax, ext=EXT, **kw):
    return ink_base(ax, CRS, ext, ripple_m=kw.pop("ripple_m", (8e3, 20e3)), coast_lw=kw.pop("coast_lw", 0.6), countries=False, min_area=kw.pop("min_area", 2e7), **kw)


def hexes(ax, H, min_reg=3, alpha_by_share=True):
    for h in H:
        p = h["properties"]
        cs = np.array([f27(x, y) for x, y in h["geometry"]["coordinates"][0]])
        if p["regional"] >= min_reg and p["top"] not in ("", "tie"):
            share = p["top_n"] / p["regional"]
            ax.add_patch(MP(cs, closed=True, fc=WCOL[p["top"]], ec=PAPER, lw=0.4, alpha=0.45 + 0.5 * share if alpha_by_share else 0.9, zorder=3.5))
        else:
            ax.add_patch(MP(cs, closed=True, fc="none", ec="#9C8656", lw=0.35, alpha=0.6, zorder=3.4))


# ---------- 1. the dominant regional word per 20 km hexagon
dom = R["hex"]["dominant"]
fig = plt.figure(figsize=(10.5, 12.5)); parchment(fig)
ax = fig.add_axes([0.0, 0.03, 0.72, 0.87])
ext, f = base(ax)
hexes(ax, H)
ax.set_xlim(ext[0] + 0.6e5, ext[1]); ax.set_ylim(ext[2], ext[3]); ax.set_facecolor("none")
fig.text(0.04, 0.955, "The word on the street sign", fontproperties=HAND, fontsize=27, color=RED, va="center")
fig.text(0.04, 0.925, f"Commonest regional alley word in each 20 km hexagon with three or more ({R['hex']['cells_regional3']} hexagons)", fontproperties=FELL, fontsize=12.5, color=INKC, va="center")
lx = fig.add_axes([0.70, 0.20, 0.29, 0.66]); lx.axis("off")
order = [w for w in REGIONAL if w in dom]
order.sort(key=lambda w: -dom[w])
for i, k in enumerate(order):
    y = 0.98 - i * 0.056
    lx.add_patch(plt.Rectangle((0, y - 0.019), 0.09, 0.038, fc=WCOL[k], ec=INKC, lw=0.4, transform=lx.transAxes))
    lx.text(0.13, y, f"{WLAB[k]}", fontproperties=FELL, fontsize=12.5, color=INKC, va="center", transform=lx.transAxes)
    lx.text(0.97, y, f"{dom[k]}", fontproperties=FELL, fontsize=11, color=MUT, va="center", ha="right", transform=lx.transAxes)
lx.text(0, 0.98 - len(order) * 0.056, "Number on the right: hexagons led.\nPaler: the leader has under half\nthe regional names. Outlined:\nnamed alleys, but fewer than three\nwith a regional word.", fontproperties=FELL, fontsize=10.5, color=MUT, va="top", transform=lx.transAxes)
for txt, lon, lat in [("wynd and close", -1.2, 57.6), ("chare", -0.9, 55.2), ("loke", 1.75, 53.15), ("jitty", 0.25, 52.98), ("ope", -6.2, 50.25), ("twitten", 0.35, 50.55)]:
    x, y = f(lon, lat)
    ax.text(x, y, txt, fontproperties=FELLIT, fontsize=12, color=INKC, path_effects=HALO, zorder=9)
fig.text(0.04, 0.015, "Data: OpenStreetMap contributors (ODbL). Names of highways only: most alleys have no official name.", fontproperties=FELL, fontsize=9.5, color=MUT)
out(fig, "hexmap")

# ---------- 2. how many of each word
W = A.word.value_counts()
order = [w for w, *_ in WORDS if w in W.index]
fig = plt.figure(figsize=(10.5, 7.6)); parchment(fig)
ax = fig.add_axes([0.2, 0.09, 0.62, 0.8])
ys = np.arange(len(order))[::-1]
for y, k in zip(ys, order):
    s = A[A.word == k]
    n, p = len(s), 100 * s.path.astype(str).isin(["True"]).mean()
    ax.barh(y, n, color=WCOL[k], ec=INKC, lw=0.4, height=0.72)
    ax.text(n * 1.1 + 0.6, y, f"{n:,}", va="center", fontproperties=FELL, fontsize=10.5, color=INKC)
    ax.text(2600, y, f"{p:.0f}%", va="center", ha="right", fontproperties=FELL, fontsize=10.5, color=MUT)
ax.text(2600, ys[0] + 0.9, "on paths", ha="right", fontproperties=FELLIT, fontsize=10, color=MUT)
ax.set_xscale("symlog", linthresh=10); ax.set_xlim(0, 2700)
ax.set_xticks([0, 10, 100, 1000]); ax.set_xticklabels(["0", "10", "100", "1,000"])
ax.set_yticks(ys); ax.set_yticklabels([WLAB[k] for k in order], fontproperties=FELL, fontsize=11.5)
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.axhline(ys[order.index("alley")] + 0.5, color=MUT, lw=0.6, ls=(0, (3, 2)))
ax.text(1.0, ys[order.index("alley")] + 0.15, "general words", fontproperties=FELLIT, fontsize=10, color=MUT, ha="left", va="bottom")
ax.set_xlabel("named alleys (log scale)", fontproperties=FELL, fontsize=11)
fig.text(0.04, 0.95, "How many named alleys carry each word", fontproperties=FELLSC, fontsize=15, color=RED)
fig.text(0.04, 0.92, "Right: the share that are footpaths, steps or pedestrian ways rather than roads.", fontproperties=FELL, fontsize=11, color=MUT)
out(fig, "words")

# ---------- 3. small multiples: one map per regional word
SM = [w for w in REGIONAL if R["words"].get(w, {}).get("n", 0) >= 7]
nc = 4; nr = math.ceil(len(SM) / nc)
fig = plt.figure(figsize=(12, 3.7 * nr + 0.9)); parchment(fig)
fig.text(0.03, 1 - 0.35 / (3.7 * nr + 0.9), "Where each word is found", fontproperties=FELLSC, fontsize=17, color=RED, va="center")
for i, k in enumerate(SM):
    r_, c_ = divmod(i, nc)
    h = (1 - 0.9 / (3.7 * nr + 0.9)) / nr
    ax = fig.add_axes([c_ / nc + 0.005, 1 - 0.9 / (3.7 * nr + 0.9) - (r_ + 1) * h + 0.005, 1 / nc - 0.01, h - 0.01])
    ext, f = base(ax, ripple_m=(), coast_lw=0.35, min_area=1e8)
    s = A[A.word == k]
    ax.scatter(s.X, s.Y, s=14, c=WCOL[k], edgecolor=INKC, lw=0.3, zorder=6)
    ax.set_xlim(ext[0] + 0.6e5, ext[1]); ax.set_ylim(ext[2], ext[3]); ax.set_facecolor("none")
    ax.text(0.03, 0.97, WLAB[k], transform=ax.transAxes, fontproperties=HAND, fontsize=17, color=RED, va="top", path_effects=HALO)
    ax.text(0.03, 0.885, f"{R['words'][k]['n']:,} alleys", transform=ax.transAxes, fontproperties=FELL, fontsize=10.5, color=INKC, va="top", path_effects=HALO)
out(fig, "small")

# ---------- 4. towns with the most named alleys
T = TW.head(15).iloc[::-1]
fig = plt.figure(figsize=(10.5, 7.2)); parchment(fig)
ax = fig.add_axes([0.25, 0.09, 0.6, 0.8])
for y, t in enumerate(T.itertuples()):
    s = A[A.town == t.town].word.value_counts()
    left = 0
    for k in [w for w, *_ in WORDS if w in s.index]:
        ax.barh(y, s[k], left=left, color=WCOL[k], ec=INKC, lw=0.3, height=0.72)
        if s[k] >= 12:
            ax.text(left + s[k] / 2, y, WLAB[k].split(" ")[0], ha="center", va="center", fontproperties=FELL, fontsize=9, color="white" if k not in ("steps", "passage", "cut", "backway") else INKC)
        left += s[k]
    ax.text(left + 4, y, f"{t.n}", va="center", fontproperties=FELL, fontsize=10.5, color=INKC)
ax.set_yticks(range(len(T))); ax.set_yticklabels(T.town, fontproperties=FELL, fontsize=11.5)
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.set_xlabel("named alleys within 6 km of the town's centre (London: all of Greater London)", fontproperties=FELL, fontsize=10.5)
fig.text(0.04, 0.95, "The towns with the most named alleys", fontproperties=FELLSC, fontsize=15, color=RED)
fig.text(0.04, 0.92, "Each bar split by the word used. London and Birmingham: passages and alleys; Scotland: wynds and closes.", fontproperties=FELL, fontsize=11, color=MUT)
out(fig, "towns")

# ---------- 5. where words meet: Wharfedale and Airedale (ginnel, snicket), Tyneside (chare, wynd, lonnen), Nottingham and Leicester
ST = settlements(1000)
LAB = [["Leeds", "Otley", "Ilkley", "Huddersfield", "Harrogate", "Halifax", "Yeadon", "Keighley"],
       ["Newcastle upon Tyne", "Durham", "Hexham", "Sunderland", "Bishop Auckland"],
       ["Brighton", "Lewes", "Haywards Heath", "Worthing", "Hastings", "East Grinstead", "Horsham", "Eastbourne"]]
fig = plt.figure(figsize=(12, 5.4)); parchment(fig)
panels = [("Leeds and Wharfedale", (-2.15, -1.2, 53.55, 54.2), ["ginnel", "snicket"], "upper left"),
          ("Tyneside and Durham", (-2.0, -1.3, 54.58, 55.07), ["chare", "wynd", "lonnen", "vennel"], "lower left"),
          ("Sussex (East and West Sussex only)", (-0.95, 0.75, 50.45, 51.3), ["twitten", "passage", "alley", "steps"], "lower right")]
for i, (title, ext_ll, ws, loc) in enumerate(panels):
    ax = fig.add_axes([i / 3 + 0.008, 0.03, 1 / 3 - 0.016, 0.82])
    ext, f = ink_base(ax, CRS, ext_ll, ripple_m=(), coast_lw=0.6, countries=False)
    for k in ws:
        s = A[(A.word == k) & A.lon.between(ext_ll[0], ext_ll[1]) & A.lat.between(ext_ll[2], ext_ll[3])]
        if i == 2:
            s = s[s.county.isin(["East Sussex", "West Sussex"])]
        ax.scatter(s.X, s.Y, s=34, c=WCOL[k], edgecolor=INKC, lw=0.4, zorder=6, label=f"{WLAB[k]} ({len(s)})")
    for nm in LAB[i]:
        r_ = ST[ST.name == nm].iloc[0]
        x, y = f(r_.lon, r_.lat)
        ax.plot(x, y, "s", ms=3.5, color=INKC, zorder=7, clip_on=True)
        ax.text(x, y + 1200, nm, fontproperties=FELL, fontsize=10, color=INKC, ha="center", va="bottom", path_effects=HALO, zorder=8, clip_on=True)
    ax.legend(loc=loc, prop=FELL, fontsize=10, frameon=True, facecolor=PAPER, edgecolor="#9C8656")
    ax.set_title(title, fontproperties=FELLSC, fontsize=13, color=RED)
fig.text(0.03, 0.95, "Where the words meet", fontproperties=FELLSC, fontsize=16, color=RED)
out(fig, "meet")
print("figures done")
