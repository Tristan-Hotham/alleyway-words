"""The alley words: spelling variants, family, label, colour and a one-line note on where the word belongs.
A name counts for a word only when the word is the head of the name (its last word, once numbers, brackets and a
trailing '- from X to Y' are removed), so 'Twitten Lane', 'Jetty Road' and 'Chare Bank' do not count.
Notes on where the words belong are the general picture in the dialect dictionaries and recent surveys of usage;
they are context for the map, not results."""

# key, label, spellings (lower case), colour, kind ('regional' or 'general'), note
WORDS = [
    ("ginnel", "ginnel", ["ginnel", "ginnell", "gennel", "jennel", "jinnel"], "#EA580C", "regional", "Lancashire, Greater Manchester and West Yorkshire"),
    ("snicket", "snicket", ["snicket", "snickets", "snickelway"], "#7C3AED", "regional", "Yorkshire and Humberside"),
    ("twitten", "twitten", ["twitten", "twittens"], "#0F766E", "regional", "Sussex"),
    ("twitchel", "twitchel", ["twitchel", "twitchell", "twitchill", "twitch"], "#65A30D", "regional", "Nottinghamshire and the East Midlands, also parts of Essex and Hertfordshire"),
    ("jitty", "jitty or gitty", ["jitty", "gitty", "jetty"], "#DB2777", "regional", "the East Midlands: Leicestershire, Derbyshire, Nottinghamshire, Northamptonshire"),
    ("chare", "chare", ["chare", "chares"], "#1D4ED8", "regional", "Newcastle, Durham and the North East"),
    ("wynd", "wynd", ["wynd", "wynds"], "#92400E", "regional", "Scotland and the North East of England"),
    ("vennel", "vennel", ["vennel", "vennal", "vennels"], "#0891B2", "regional", "Scotland and the North East of England"),
    ("close", "close (Scotland)", ["close"], "#D4A017", "regional", "Scotland: the narrow entries off the old high streets"),
    ("pend", "pend", ["pend"], "#9D174D", "regional", "Scotland: a passage through a building"),
    ("entry", "entry", ["entry", "entries"], "#4D7C0F", "regional", "Merseyside, Birmingham and the West Midlands, Lancashire, Belfast"),
    ("loke", "loke", ["loke", "lokes"], "#B91C1C", "regional", "Norfolk and Suffolk"),
    ("jigger", "jigger", ["jigger", "jiggers"], "#6D28D9", "regional", "Liverpool"),
    ("shut", "shut", ["shut", "shuts"], "#A21CAF", "regional", "Shrewsbury and Shropshire"),
    ("ope", "ope", ["ope", "opes"], "#0284C7", "regional", "Plymouth and Devon, also Cornwall"),
    ("drang", "drang or drong", ["drang", "drong", "drangway"], "#15803D", "regional", "Devon and the West of England"),
    ("lonnen", "lonnen", ["lonnen", "lonning", "lonnin"], "#57534E", "regional", "the North East and Cumbria (a lane)"),
    ("gully", "gully", ["gully", "gulley", "gullies"], "#CA8A04", "regional", "Birmingham and the Black Country"),
    ("tenfoot", "tenfoot", ["tenfoot"], "#334155", "regional", "Hull, the East Riding and north Lincolnshire"),
    ("alley", "alley", ["alley", "alleyway", "alleys"], "#64748B", "general", "standard English"),
    ("passage", "passage", ["passage"], "#94A3B8", "general", "standard English"),
    ("steps", "steps", ["steps"], "#A8A29E", "general", "standard English, often steep towns"),
    ("backway", "backway", ["backway", "backways"], "#B8A99A", "general", "standard English: a way round the back"),
    ("cut", "cut", ["cut"], "#CBD5E1", "general", "standard English: a short cut"),
    ("slype", "slype", ["slype"], "#78716C", "general", "a passage by a cathedral or abbey (an architectural word)"),
]
WMAP = {s: w[0] for w in WORDS for s in w[2]}
WCOL = {w[0]: w[3] for w in WORDS}
WLAB = {w[0]: w[1] for w in WORDS}
WKIND = {w[0]: w[4] for w in WORDS}
WNOTE = {w[0]: w[5] for w in WORDS}
REGIONAL = [w[0] for w in WORDS if w[4] == "regional"]

PATH_TYPES = {"footway", "pedestrian", "path", "steps", "cycleway", "bridleway", "corridor", "living_street", "service", "track"}
