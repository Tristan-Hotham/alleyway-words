# Ginnel, snicket or twitten?

The regional words for an alley on the street signs of the United Kingdom. 30,481 OpenStreetMap highways whose names contain an alley word; names kept when the alley word is the head of the name; pieces of one alley joined; false friends removed after reading every alley of the ambiguous words; 3,382 named alleys mapped by word, county, town and 20 km hexagon.

Interactive page: https://maps.tristanhotham.com/alleyway-words/
Paper: https://doi.org/10.5281/zenodo.24086513
Blog post: https://blog.tristanhotham.com/2026/10/31/alleyway-words/
Code and data: https://github.com/Tristan-Hotham/alleyway-words

## Headline results

- 3,382 named alleys: 1,795 with a regional word, 1,587 with a general one (alley, passage, steps, backway, cut).
- Scotland names its alleys with regional words, nearly all Scots (94% of 1,294); England rarely uses a regional word (28% of 2,016); London almost never (2 of 375).
- Regional words stay at home: 88% of 33 twittens in Sussex; 98% of 188 lokes in Norfolk and Suffolk; all 45 chares in the North East (15 in Newcastle); 97% of 32 opes in Devon, Cornwall and Dorset (15 in Plymouth); all 6 shuts in Shropshire; 78% of 32 jitties in the East Midlands.
- The wynd is the commonest word (957) but now mostly a road name on new estates (78% roads). 85 of 253 Scottish closes are in Edinburgh.
- Yorkshire: 14 ginnels (Leeds, Huddersfield, Harrogate, Skipton) and 10 snickets, 7 of them around Burley in Wharfedale, 9.1 km from the nearest ginnel.
- The back-alley words barely reach the sign: no alley named jigger anywhere (Liverpool included), 1 tenfoot, no gully in Birmingham.

## Files

| File | What it is |
|---|---|
| `index.html`, `js/page.js` | The interactive page: MapLibre on the OpenFreeMap Positron base map, every named alley coloured by its word, a word picker, 20 km hexagons, search and popups. |
| `header.png` | Social card, 1200 x 630. |
| `data/alleys.csv` | Every named alley (3,382): id, word, name, position (first point of the alley's ways), county, nation, nearest town, number of OSM ways, highway types, footpath or not, OSM way ids. ODbL. |
| `data/alleys.json`, `data/places.json`, `data/hexagons.geojson` | Page data. ODbL / CC0. |
| `data/by_county.csv`, `data/towns.csv`, `data/hexagons.csv` | Counts by county, town and 20 km hexagon. |
| `data/results.json` | Every number quoted on the page, in the paper, blog, collage and post. |
| `img/` | Figures on the page. |
| `code/` | Numbered scripts, `words.py` (the words and spellings), `overrides.csv` (false friends removed by hand), templates, `qa.js`. |
| `release/` | Paper (`paper/`), blog post and figures (`blog/`), Zenodo files (`zenodo/`). |
| `reddit/` | Collage (`collage.py`, PNG) and post text. |

## Method in brief

- Head word: the last word of the name once numbers, brackets and route notes are removed (Twitten Lane does not count; The Twitten does). Close only for footpaths in Scotland.
- Pieces of one name joined when their first points chain within 150 m (600 m for roads and names with a specific part); 3,256 ways joined.
- False friends: jetty counts as jitty only in the East Midlands; cut only as a footpath and never New Cut; hill-path steps out; a cut with any road piece out; 61 more removed by hand (`code/overrides.csv`: cave passages, mountain-bike trails, Tarr Steps and the like); three misspelt or doubled names joined (`code/renames.csv`). 159 of 3,541 candidates removed in all.
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

Hotham, T. (2026) Ginnel, snicket or twitten? The regional words for an alley on the street signs of the United Kingdom. Zenodo. https://doi.org/10.5281/zenodo.24086513

Dr Tristan Hotham, Independent researcher. ORCID 0000-0003-4931-9349.

I wrote the text, with drafting and editing assistance from Claude (Anthropic), which also helped prepare the analysis code. I reviewed and checked all text and results.
