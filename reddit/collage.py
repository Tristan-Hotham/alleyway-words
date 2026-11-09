"""Reddit collage (r/dataisbeautiful style) and the 1200 x 630 header card.
Light parchment background; labels on the sea; full legend; source footer.
Output: reddit/alleyway_words_collage.png (3000 x 2100 px) and header.png. Run after code/04_figures.py."""
import os, sys, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "code"))
import pandas as pd
import matplotlib.patheffects as pe
from matplotlib.patches import Polygon as MP
from figstyle import *
from words import WCOL, WLAB, REGIONAL

R = jload(f"{DATA}/results.json")
H = jload(f"{DATA}/hexagons.geojson")["features"]
W = R["words"]
HALO = [pe.withStroke(linewidth=3, foreground=PAPER)]
OUT = os.path.join(ROOT, "reddit", "alleyway_words_collage.png")
f27 = projector(27700)


def hexmap(ax, ext_ll=(-8.0, 1.95, 49.9, 58.9), lw=0.35):
    ext, f = ink_base(ax, 27700, ext_ll, coast_lw=0.5, ripple_m=(6e3, 15e3), countries=False, min_area=2e7)
    for h in H:
        p = h["properties"]
        cs = np.array([f27(x, y) for x, y in h["geometry"]["coordinates"][0]])
        if p["regional"] >= 3 and p["top"] not in ("", "tie"):
            ax.add_patch(MP(cs, closed=True, fc=WCOL[p["top"]], ec=PAPER, lw=lw, alpha=0.45 + 0.5 * p["top_n"] / p["regional"], zorder=3.5))
        else:
            ax.add_patch(MP(cs, closed=True, fc="none", ec="#9C8656", lw=0.3, alpha=0.5, zorder=3.4))
    ax.set_xlim(ext[0] + 0.6e5, ext[1]); ax.set_ylim(ext[2], ext[3]); ax.set_facecolor("none")
    return ext, f


fig = plt.figure(figsize=(10, 7), dpi=300); parchment(fig, seed=11)
fig.text(0.035, 0.955, "Ginnel, snicket or twitten?", fontproperties=HAND, fontsize=30, color=RED, va="center")
fig.text(0.035, 0.912, f"Britain's words for an alley, on the street signs: {R['n']['alleys']:,} named alleys in the UK, by the word in their name", fontproperties=FELL, fontsize=12, color=INKC, va="center")
fig.text(0.035, 0.885, "Official street names from OpenStreetMap, not speech. Most alleys have no name at all.", fontproperties=FELL, fontsize=10, color=MUT, va="center")
ax = fig.add_axes([0.0, 0.05, 0.47, 0.81])
ext, f = hexmap(ax)
for txt, lon, lat in [("wynd and close", -0.9, 57.2), ("chare", 0.0, 55.25), ("loke", 1.95, 53.25), ("jitty", 0.75, 53.6), ("twitten", 0.55, 50.45), ("ope", -6.75, 50.3)]:
    x, y = f(lon, lat)
    ax.text(x, y, txt, fontproperties=FELLIT, fontsize=10.5, color=INKC, path_effects=HALO, zorder=9)
dom = R["hex"]["dominant"]
order = sorted([w for w in REGIONAL if w in dom], key=lambda w: -dom[w])
lx = fig.add_axes([0.445, 0.15, 0.14, 0.71]); lx.axis("off")
lx.text(0, 1.0, "Commonest regional\nword per 20 km hexagon", fontproperties=FELLSC, fontsize=9.5, color=RED, va="top")
for i, k in enumerate(order):
    y = 0.9 - i * 0.052
    lx.add_patch(plt.Rectangle((0, y - 0.017), 0.1, 0.034, fc=WCOL[k], ec=INKC, lw=0.4, transform=lx.transAxes))
    lx.text(0.15, y, WLAB[k], fontproperties=FELL, fontsize=9, color=INKC, va="center", transform=lx.transAxes)
lx.text(0, 0.9 - len(order) * 0.052, "Outlined: named alleys,\nbut under three with a\nregional word", fontproperties=FELLIT, fontsize=7.6, color=MUT, va="top", transform=lx.transAxes)

# ---- every word stays at home
fig.text(0.62, 0.855, "Every word stays at home", fontproperties=FELLSC, fontsize=13, color=RED)
fig.text(0.62, 0.832, "Share of each word's named alleys in its home region", fontproperties=FELL, fontsize=9, color=MUT)
HOME = [("chare", "North East England"), ("shut", "Shropshire"), ("loke", "Norfolk and Suffolk"), ("ope", "Devon, Cornwall, Dorset"),
        ("lonnen", "North East and Cumbria"), ("ginnel", "northern England"), ("twitten", "Sussex"), ("jitty", "East Midlands"), ("snicket", "Yorkshire")]
bx = fig.add_axes([0.745, 0.47, 0.17, 0.35])
for i, (k, reg) in enumerate(HOME):
    y = len(HOME) - 1 - i
    bx.barh(y, 100, color="#E9DDBD", height=0.62, edgecolor="none")
    bx.barh(y, W[k]["home_pc"], color=WCOL[k], height=0.62, edgecolor=INKC, lw=0.4)
    bx.text(-4, y + 0.1, f"{WLAB[k].split(' ')[0]}", ha="right", va="center", fontproperties=FELL, fontsize=10, color=INKC)
    bx.text(-4, y - 0.3, reg, ha="right", va="center", fontproperties=FELLIT, fontsize=6.8, color=MUT)
    bx.text(103, y, f"{W[k]['home_pc']:.0f}%  of {W[k]['n']}", va="center", fontproperties=FELL, fontsize=8.5, color=INKC)
bx.set_xlim(0, 100); bx.set_ylim(-0.6, len(HOME) - 0.4); bx.axis("off")

# ---- Scotland, England, London
fig.text(0.62, 0.40, "Who uses a regional word at all?", fontproperties=FELLSC, fontsize=13, color=RED)
NAT = [("Scotland", R["nations"]["Scotland"]["regional_pc"], R["nations"]["Scotland"]["n"]), ("England", R["nations"]["England"]["regional_pc"], R["nations"]["England"]["n"]),
       ("Wales", R["nations"]["Wales"]["regional_pc"], R["nations"]["Wales"]["n"]), ("London", 100 * R["london"]["regional_n"] / R["london"]["n"], R["london"]["n"])]
nx = fig.add_axes([0.70, 0.21, 0.2, 0.16])
for i, (nm, pc, n) in enumerate(NAT):
    y = 3 - i
    nx.barh(y, 100, color="#E9DDBD", height=0.6, edgecolor="none")
    nx.barh(y, pc, color=RED if nm != "London" else "#64748B", height=0.6, edgecolor=INKC, lw=0.4)
    nx.text(-4, y, nm, ha="right", va="center", fontproperties=FELL, fontsize=10, color=INKC)
    nx.text(103, y, f"{pc:.0f}%  of {n:,}", va="center", fontproperties=FELL, fontsize=8.5, color=INKC)
nx.set_xlim(0, 100); nx.axis("off")
fig.text(0.62, 0.18, f"London: {R['london']['n']} named alleys, {R['london']['passage_n']} passages, {R['london']['alley_n']} alleys,\nonly {R['london']['regional_n']} with a regional word. "
         f"{R['wynd']['road_pc']:.0f}% of the {W['wynd']['n']} wynds are now\nroads, many on new estates. The back-alley words never made\nthe sign: no jigger in Liverpool, {W['tenfoot']['n']} tenfoot near Hull, no gully\nin Birmingham.", fontproperties=FELL, fontsize=8.8, color=INKC, va="top")
fig.text(0.035, 0.034, "Data: OpenStreetMap contributors (ODbL), via QLever; Wikidata (CC0). Names whose last word is the alley word; pieces of one alley joined;", fontproperties=FELL, fontsize=7.4, color=MUT)
fig.text(0.035, 0.016, f"false friends removed by rule and by hand ({R['n']['dropped']} of {R['n']['candidates']:,}): a jetty counts as a jitty only in the East Midlands. Close counted only for Scottish footpaths.", fontproperties=FELL, fontsize=7.4, color=MUT)
fig.text(0.965, 0.018, "maps.tristanhotham.com/alleyway-words", fontproperties=FELL, fontsize=8, color=RED, ha="right")
fig.savefig(OUT, dpi=300, facecolor=fig.get_facecolor())
plt.close(fig)

# ---- header card 1200 x 630
fig = plt.figure(figsize=(12, 6.3), dpi=100); parchment(fig, seed=5)
ax = fig.add_axes([0.52, 0.0, 0.48, 1.0])
hexmap(ax, ext_ll=(-6.6, 1.9, 50.0, 58.7), lw=0.3)
fig.text(0.05, 0.78, "Ginnel, snicket", fontproperties=HAND, fontsize=50, color=INKC)
fig.text(0.05, 0.64, "or twitten?", fontproperties=HAND, fontsize=50, color=RED)
fig.text(0.05, 0.50, f"Britain's {R['n']['alleys']:,} named alleys,", fontproperties=FELL, fontsize=22, color=INKC)
fig.text(0.05, 0.44, "by the word on the street sign", fontproperties=FELL, fontsize=22, color=INKC)
fig.text(0.05, 0.30, f"{W['twitten']['home_pc']:.0f}% of twittens are in Sussex.", fontproperties=FELLIT, fontsize=19, color=RED)
fig.text(0.05, 0.24, f"Every chare is in the North East.", fontproperties=FELLIT, fontsize=19, color=RED)
fig.text(0.05, 0.08, "Dr Tristan Hotham · maps.tristanhotham.com/alleyway-words", fontproperties=FELL, fontsize=13, color=MUT)
fig.savefig(os.path.join(ROOT, "header.png"), dpi=100, facecolor=fig.get_facecolor())
from PIL import Image
im = Image.open(os.path.join(ROOT, "header.png")); assert im.size == (1200, 630), im.size
print("collage", Image.open(OUT).size)
