"""Step 8: blog post and meta (release/blog), Zenodo files and metadata (release/zenodo).
10.5281/zenodo.24086513, https://doi.org/10.5281/zenodo.24086513 and https://blog.tristanhotham.com/2026/10/31/alleyway-words/ stay as placeholders for the publisher."""
import shutil, zipfile, importlib.util
from PIL import Image
from common import *

spec = importlib.util.spec_from_file_location("b", os.path.join(ROOT, "code", "06_build_site.py"))
spec.loader.exec_module(importlib.util.module_from_spec(spec))          # shared fact checks (and rebuilds index.html)
R = jload(f"{DATA}/results.json")
REL = os.path.join(ROOT, "release"); NAME = "Hotham_Alleyway_Words"
KEEP = {"DOI", "DOI_URL", "BLOG_URL"}

post = fill(open(os.path.join(ROOT, "code", "blog_template.html"), encoding="utf-8").read(), R)
used = re.findall(r"\{\{IMG\|([^|]+)\|", post)
assert 5 <= len(used) <= 8, len(used)
assert all(re.search(r"^\{\{IMG\|" + re.escape(u_), post, re.M) for u_ in used) and "wp:image" not in post
for img in used:
    assert Image.open(f"{REL}/blog/{img}").size[0] == 1800, img
for fn in os.listdir(f"{REL}/blog"):
    if fn.startswith("b_") and fn not in used:
        os.remove(f"{REL}/blog/{fn}")
assert set(re.findall(r"\{\{([^|}]+)\}\}", post)) <= KEEP, set(re.findall(r"\{\{([^|}]+)\}\}", post))
vis = re.sub(r"<!--.*?-->", "", post, flags=re.S)
for bad in ("\u2014", "\u2013", "--", "DSIT", "DCMS", "civil serv"):
    assert bad not in vis, bad
assert AI in post
open(f"{REL}/blog/post.html", "w", encoding="utf-8").write(post)
words = len(re.sub(r"<[^>]+>|\{\{IMG\|[^}]*\}\}", " ", vis).split())
W = R["words"]
meta = {"title": "Ginnel, snicket or twitten? Britain's alley words on the street signs",
        "slug": "alleyway-words",
        "excerpt": f"I mapped all {R['n']['alleys']:,} named alleys in the UK by the word in their name. {W['twitten']['home_pc']:.0f}% of twittens are in Sussex, every chare is in the North East, and London's {R['london']['n']} named alleys use a regional word just {R['london']['regional_n']} times.",
        "seo_description": f"Every named alley in the UK mapped by its word: twitten, ginnel, snicket, jitty, chare, wynd, loke, ope. {W['twitten']['home_pc']:.0f}% of twittens are in Sussex.",
        "tags": ["maps", "dialect", "street names", "alleys", "place names", "Scots", "OpenStreetMap", "data visualisation", "language"],
        "header_alt": f"Title card reading 'Ginnel, snicket or twitten?' beside a map of Britain in coloured hexagons for the commonest alley word, wynd in Scotland, chare on Tyneside, loke in Norfolk and twitten in Sussex, with the line {W['twitten']['home_pc']:.0f}% of twittens are in Sussex."}
assert len(meta["seo_description"]) < 160, len(meta["seo_description"])
jsave(meta, f"{REL}/blog/meta.json", indent=2)

Z = f"{REL}/zenodo"; os.makedirs(Z, exist_ok=True)
for fn in os.listdir(Z):
    os.remove(os.path.join(Z, fn))
shutil.copy(f"{REL}/paper/{NAME}.pdf", f"{Z}/{NAME}.pdf")
zp = f"{Z}/{SLUG}_data_and_code.zip"
with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
    for dd in ("code", "js"):
        for fn in sorted(os.listdir(os.path.join(ROOT, dd))):
            if fn.endswith(".pyc") or fn == "__pycache__" or fn.endswith(".png"):
                continue
            z.write(os.path.join(ROOT, dd, fn), f"{SLUG}/{dd}/{fn}")
    for fn in sorted(os.listdir(os.path.join(ROOT, "data"))):
        z.write(os.path.join(ROOT, "data", fn), f"{SLUG}/data/{fn}")
    for fn in ("README.md", "LICENSE", "index.html"):
        z.write(os.path.join(ROOT, fn), f"{SLUG}/{fn}")
    z.write(os.path.join(ROOT, "reddit", "collage.py"), f"{SLUG}/reddit/collage.py")
tex = open(f"{REL}/paper/{NAME}.tex", encoding="utf-8").read()
ab = re.search(r"\\begin\{center\}\\textbf\{Abstract\}\\end\{center\}\n(.*?)\n\n\\textbf\{Keywords", tex, re.S).group(1)
ab = ab.replace("\\%", "%").replace("\\&", "&")
ab = re.sub(r"\\textit\{([^}]*)\}", r"\1", ab)
assert "\\" not in ab and "$" not in ab, ab
zmeta = {"title": "Ginnel, Snicket or Twitten? The Regional Words for an Alley on the Street Signs of the United Kingdom",
         "upload_type": "publication", "publication_type": "workingpaper",
         "description": f"<p>{ab}</p><p>Interactive page: <a href=\"{PAGE}\">{PAGE}</a>. Data and code: <a href=\"{REPO}\">{REPO}</a>. Blog post: {{https://blog.tristanhotham.com/2026/10/31/alleyway-words/}}.</p><p>Sources: OpenStreetMap contributors (ODbL), queried with QLever; Wikidata (CC0); ONS boundaries (OGL v3.0). The alley tables are derived from OpenStreetMap and released under the Open Database Licence; text and figures CC BY 4.0; code MIT.</p>",
         "creators": [{"name": "Hotham, Tristan", "affiliation": "Independent researcher", "orcid": "0000-0003-4931-9349"}],
         "keywords": ["dialect geography", "street names", "toponymy", "alleys", "Scots", "English dialects", "OpenStreetMap"],
         "license": "cc-by-4.0", "language": "eng",
         "notes": "Text and figures CC BY 4.0; code MIT; data/alleys.csv, alleys.json and the other alley tables derived from OpenStreetMap, ODbL.",
         "related_identifiers": [{"identifier": REPO, "relation": "isSupplementedBy", "resource_type": "software"},
                                 {"identifier": PAGE, "relation": "isSupplementedBy", "resource_type": "other"},
                                 {"identifier": "https://www.openstreetmap.org/", "relation": "isDerivedFrom", "resource_type": "dataset"}],
         "files": sorted(os.listdir(Z))}
sj = json.dumps(zmeta, ensure_ascii=False) + json.dumps(meta, ensure_ascii=False)
assert "\u2014" not in sj and "\u2013" not in sj and "--" not in sj and "https://blog.tristanhotham.com/2026/10/31/alleyway-words/" in sj
jsave(zmeta, f"{Z}/metadata.json", indent=2)
print("blog words", words, "figures", len(used), "; zenodo", sorted(os.listdir(Z)), os.path.getsize(zp) // 1024, "KB zip")
