# alleyway-words: working notes

Brief: /home/claude/work/new10/BRIEFS.md (study 1) + shared rules in new8/new9 BRIEFS.md and /home/claude/newdata/BRIEF.md.
Format refs: studies/river-names (code layout), studies/tower-shadows (plain MapLibre Positron basemap).
Work files: /home/claude/scratch/alleyway-words (delete at the end).

## Log
- Set up folder; data explored (30,481 OSM ways in streets_uk.tsv.gz; shared with battle-streets).
- Pipeline: 01_alleys (head words, join pieces 150 m / 600 m) -> 02_review (false friends: rules + code/overrides.csv) -> 03_analysis
  (results.json, towns, counties, 20 km hexagons) -> 04_figures -> 05_export -> 06_build_site -> 07_paper -> reddit/collage.py
  -> 09_readme -> 08_release -> qa.js.

## Data checks (whole set)
- Every alley of the ambiguous words (jetty/jitty, cut, entry, gully, shut, ope, steps, drang, tenfoot/backway, twitchel,
  snicket, ginnel, twitten, chare, lonnen, pend, vennel, close) read by eye from WORK/review_*.txt with highway type, county
  and nearest town. Rules + 27 hand drops; 125 of 3,544 candidates removed (3.5%). Wynd, passage, alley, steps checked by
  county distribution and name lists only (big, unambiguous groups).
- Polygon ways (pedestrian areas, 338 rows) were first lost by the WKT parser; fixed (POLYGON first point now read).
- London districts typed as towns in Wikidata (Stepney, Fulham) split London: all Greater London alleys now count as London.
- 'tenfoot' and 'backway' split (backway is a general word).

## References and claims to verify (cited from memory)
- Wright, J. (1898 to 1905) The English Dialect Dictionary. London: Henry Frowde.
- Orton, H. and Dieth, E. (1962 to 1971) Survey of English Dialects: The Basic Material. Leeds: E. J. Arnold.
- Upton, C., Sanderson, S. and Widdowson, J. (1987) Word Maps: A Dialect Atlas of England. London: Croom Helm.
- Upton, C., Parry, D. and Widdowson, J. D. A. (1994) Survey of English Dialects: The Dictionary and Grammar. London: Routledge.
- Upton, C. and Widdowson, J. D. A. (1996) An Atlas of English Dialects. Oxford: OUP.
- Dictionary of the Scots Language (dsl.ac.uk).
- Haklay, M. (2010) How good is volunteered geographical information? Environment and Planning B 37(4), 682 to 703.
- Bast, H. and Buchhold, B. (2017) QLever, CIKM 2017, 647 to 656.
- Jones, M. W. (1983) A Walk Around the Snickelways of York (self-published): the coining of 'snickelway'. CHECK title/year.
- Regional labels in code/words.py ("usually ...") are the general picture from the dictionaries, not checked against
  specific SED maps: twitten Sussex; snicket Yorkshire; ginnel Lancs/GM/W Yorks; twitchel Notts/Derbys/Lincs; jitty East
  Midlands; chare NE; wynd/close/vennel/pend Scotland; entry Belfast/Liverpool/W Midlands/Borders; loke Norfolk/Suffolk;
  jigger Liverpool; shut Shrewsbury; ope Plymouth/Devon/Cornwall; drang West Country; lonnen Northumberland/Cumbria; gully
  Birmingham; tenfoot Hull.
- Belfast entries 'off High Street and Ann Street' (paper), Edinburgh closes off the Royal Mile, Newcastle chares on the Quayside.
- Links: maps.tristanhotham.com/street-names/ (given in brief), maps.tristanhotham.com/bread-rolls/ (from dinner-or-tea README).

## Status
- All files built; QA desktop + phone screenshots in qa/, 0 console errors.

## Independent review (2026)
- Re-ran 01 to 03: reproduced the builder's results.json exactly before changes.
- Whole-set reading found: The Cut in Southwark (a street with a primary road piece) kept as a cut; 16 cave passages
  (Mynydd Llangatwg, Powys) and mountain-bike trails called Alley/Steps kept; Tarr Steps (clapper bridge) and hill paths
  called Steps kept; duplicates Denbton/Denton Chare, Leven/Leven's Close, Ginnel/Charles Street Ginnel; slype marked
  regional though it is an architectural word.
- Fixes: cut rule now refuses any road piece; overrides.csv gains optional lat/lon and 30 new drops; code/renames.csv
  joins the three duplicates before merging; slype made general; word notes revised to what could be verified (Wikipedia
  'Alley', YouGov alley survey); texts no longer claim the SED/Upton atlases map these words; jigger absence stated as
  absent among names containing the word; Scotland share described as regional words "nearly all" wynd/close/vennel/pend
  (the four are 91%, entries make up most of the rest).
- References verified online: Word Maps (Croom Helm 1987), Atlas of English Dialects (OUP 1996), Jones 1983 snickelway.
- Known, left: nearest-town-point assignment (Johnston Terrace Ope in Plymouth's Keyham counted to Saltash; noted in paper);
  modern estate 'Entry' road names in Perthshire kept (could not verify either way).
