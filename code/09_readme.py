"""Step 9: README.md, LICENSE and the Reddit post text (reddit/post.md), filled from data/results.json."""
from common import *

R = jload(f"{DATA}/results.json")
W, N = R["words"], R["n"]
readme = f"""# Ginnel, snicket or twitten?

The regional words for an alley on the street signs of the United Kingdom. {N['ways_raw']:,} OpenStreetMap highways whose names contain an alley word; names kept when the alley word is the head of the name; pieces of one alley joined; false friends removed after reading every alley of the ambiguous words; {N['alleys']:,} named alleys mapped by word, county, town and 20 km hexagon.

Interactive page: {PAGE}
Paper: {{https://doi.org/10.5281/zenodo.24086513}}
Blog post: {{https://blog.tristanhotham.com/2026/10/31/alleyway-words/}}
Code and data: {REPO}

## Headline results

- {N['alleys']:,} named alleys: {N['regional']:,} with a regional word, {N['general']:,} with a general one (alley, passage, steps, backway, cut).
- Scotland names its alleys with regional words, nearly all Scots ({R['nations']['Scotland']['regional_pc']:.0f}% of {R['nations']['Scotland']['n']:,}); England rarely uses a regional word ({R['nations']['England']['regional_pc']:.0f}% of {R['nations']['England']['n']:,}); London almost never ({R['london']['regional_n']} of {R['london']['n']}).
- Regional words stay at home: {W['twitten']['home_pc']:.0f}% of {W['twitten']['n']} twittens in Sussex; {W['loke']['home_pc']:.0f}% of {W['loke']['n']} lokes in Norfolk and Suffolk; all {W['chare']['n']} chares in the North East ({W['chare']['top_town_n']} in Newcastle); {W['ope']['home_pc']:.0f}% of {W['ope']['n']} opes in Devon, Cornwall and Dorset ({W['ope']['top_town_n']} in Plymouth); all {W['shut']['n']} shuts in Shropshire; {W['jitty']['home_pc']:.0f}% of {W['jitty']['n']} jitties in the East Midlands.
- The wynd is the commonest word ({W['wynd']['n']}) but now mostly a road name on new estates ({R['wynd']['road_pc']:.0f}% roads). {R['close']['edinburgh_n']} of {W['close']['n']} Scottish closes are in Edinburgh.
- Yorkshire: {R['yorks']['ginnel']} ginnels (Leeds, Huddersfield, Harrogate, Skipton) and {R['yorks']['snicket']} snickets, {R['wharfedale']['snicket']} of them around Burley in Wharfedale, {R['wharfedale']['min_km']:.1f} km from the nearest ginnel.
- The back-alley words barely reach the sign: no alley named jigger anywhere (Liverpool included), {W['tenfoot']['n']} tenfoot, no gully in Birmingham.

## Files

| File | What it is |
|---|---|
| `index.html`, `js/page.js` | The interactive page: MapLibre on the OpenFreeMap Positron base map, every named alley coloured by its word, a word picker, 20 km hexagons, search and popups. |
| `header.png` | Social card, 1200 x 630. |
| `data/alleys.csv` | Every named alley ({N['alleys']:,}): id, word, name, position (first point of the alley's ways), county, nation, nearest town, number of OSM ways, highway types, footpath or not, OSM way ids. ODbL. |
| `data/alleys.json`, `data/places.json`, `data/hexagons.geojson` | Page data. ODbL / CC0. |
| `data/by_county.csv`, `data/towns.csv`, `data/hexagons.csv` | Counts by county, town and 20 km hexagon. |
| `data/results.json` | Every number quoted on the page, in the paper, blog, collage and post. |
| `img/` | Figures on the page. |
| `code/` | Numbered scripts, `words.py` (the words and spellings), `overrides.csv` (false friends removed by hand), templates, `qa.js`. |
| `release/` | Paper (`paper/`), blog post and figures (`blog/`), Zenodo files (`zenodo/`). |
| `reddit/` | Collage (`collage.py`, PNG) and post text. |

## Method in brief

- Head word: the last word of the name once numbers, brackets and route notes are removed (Twitten Lane does not count; The Twitten does). Close only for footpaths in Scotland.
- Pieces of one name joined when their first points chain within 150 m (600 m for roads and names with a specific part); {N['merged_ways']:,} ways joined.
- False friends: jetty counts as jitty only in the East Midlands; cut only as a footpath and never New Cut; hill-path steps out; a cut with any road piece out; {N['dropped_by_hand']} more removed by hand (`code/overrides.csv`: cave passages, mountain-bike trails, Tarr Steps and the like); three misspelt or doubled names joined (`code/renames.csv`). {N['dropped']} of {N['candidates']:,} candidates removed in all.
- Towns: nearest Wikidata town of 10,000 or more within 6 km; Greater London as one.
- Caveats: street names are official names, not speech; most alleys are unnamed; OSM naming is uneven; small counts for the rarer words.

## How to rerun

Needs Python 3 with pandas, numpy, scipy, geopandas, pyproj, shapely, matplotlib, Pillow; xelatex, pdftotext, pdfinfo; node with Playwright for `code/qa.js`. Raw inputs are listed in `code/common.py`; intermediates go to `AW_WORK`.

```
python3 code/01_alleys.py      # ways, head words, joined alleys
python3 code/02_review.py      # false friends out, towns
python3 code/03_analysis.py    # results.json and tables
python3 code/04_figures.py     # figures
python3 code/05_export.py      # page data
python3 code/06_build_site.py  # index.html
python3 code/07_paper.py       # paper PDF (DOI=10.5281/zenodo.N to fill the DOI)
python3 reddit/collage.py      # collage and header
python3 code/09_readme.py      # README, LICENSE, Reddit post
python3 code/08_release.py     # blog post, Zenodo files
```

## Sources and licences

- OpenStreetMap (https://www.openstreetmap.org/), © OpenStreetMap contributors, Open Database Licence, queried with QLever (University of Freiburg). The alley tables are derived databases under the ODbL.
- Wikidata (CC0) for towns; ONS boundaries (Open Government Licence v3.0) for counties.
- Dialect background: Wright (1898 to 1905), Orton and Dieth (1962 to 1971), Upton, Sanderson and Widdowson (1987), Upton, Parry and Widdowson (1994), Upton and Widdowson (1996), the Dictionary of the Scots Language. Full references in the paper.
- Base map: OpenFreeMap Positron (OpenStreetMap data, ODbL). MapLibre GL JS (BSD 3-Clause). Fonts: Fraunces, Source Serif 4, IBM Plex Mono, MedievalSharp, IM Fell (SIL Open Font License).

## Citation

Hotham, T. (2026) Ginnel, snicket or twitten? The regional words for an alley on the street signs of the United Kingdom. Zenodo. {{https://doi.org/10.5281/zenodo.24086513}}

Dr Tristan Hotham, Independent researcher. ORCID 0000-0003-4931-9349.

{AI}
"""
for bad in ("—", "–", "--", "DSIT", "DCMS"):
    assert bad not in "\\n".join(l for l in readme.replace("```", "").splitlines() if not l.startswith("|---")), bad
open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8").write(readme)
lic = open("/home/claude/studies/river-names/LICENSE", encoding="utf-8").read()
lic = lic.split("Text and figures:")[0] + """Text and figures: CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), Tristan Hotham, 2026.
Alley data (data/alleys.csv, alleys.json, hexagons.geojson, hexagons.csv, towns.csv, by_county.csv): derived from OpenStreetMap, © OpenStreetMap contributors, Open Database Licence 1.0 (https://opendatacommons.org/licenses/odbl/1-0/).
data/places.json: from Wikidata (CC0). data/results.json: CC BY 4.0.
Fonts under the SIL Open Font License.
"""
open(os.path.join(ROOT, "LICENSE"), "w", encoding="utf-8").write(lic)
post = f"""**Title:** [OC] Ginnel, snicket or twitten? I mapped all {N['alleys']:,} named alleys in the UK by the word in their name: {W['twitten']['home_pc']:.0f}% of twittens are in Sussex, every chare is in the North East

**Body:**

Britain has dozens of words for the narrow path between houses. I wanted to see which ones made it onto actual street names, so I took every OpenStreetMap highway in the UK whose name ends in an alley word, joined the pieces, removed false friends (a jetty is usually a pier) and mapped the result.

- Every word stays at home: {W['twitten']['home_pc']:.0f}% of twittens in Sussex, {W['loke']['home_pc']:.0f}% of lokes in Norfolk and Suffolk, all {W['chare']['n']} chares in the North East, {W['ope']['top_town_n']} of {W['ope']['n']} opes in Plymouth, all {W['shut']['n']} shuts in Shropshire.
- Scotland names its alleys in its own words ({R['nations']['Scotland']['regional_pc']:.0f}% use a regional word, nearly all wynd, close, vennel or pend). London has {R['london']['n']} named alleys and only {R['london']['regional_n']} use a regional word: the rest are passages, alleys and steps.
- The wynd is the commonest word, but {R['wynd']['road_pc']:.0f}% of wynds are now roads on new estates.
- Ginnel vs snicket: the ginnels are around Leeds and Huddersfield; most of Yorkshire's named snickets are a cluster of paths in Wharfedale.
- The back-alley words never made it: no alley named jigger anywhere, Liverpool included, one tenfoot near Hull, no gully in Birmingham.

Caveat: these are official street names, not speech, and most alleys have no name at all.

Interactive map (pick a word, search your town): {PAGE}

**Source comment:**

Data: OpenStreetMap contributors (ODbL) via QLever; towns from Wikidata (CC0). Tools: Python (pandas, geopandas, matplotlib), MapLibre with OpenFreeMap tiles. Every rule and hand decision is in the repo: {REPO}
"""
for bad in ("—", "–", "--"):
    assert bad not in post, bad
open(os.path.join(ROOT, "reddit", "post.md"), "w", encoding="utf-8").write(post)
print("README, LICENSE, post written")
