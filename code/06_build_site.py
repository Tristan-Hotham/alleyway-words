"""Step 6: index.html from code/page_template.html, filled from data/results.json, with the facts stated in words checked.
10.5281/zenodo.24086513, https://doi.org/10.5281/zenodo.24086513 and https://blog.tristanhotham.com/2026/10/31/alleyway-words/ stay as placeholders for the publisher."""
import time
import pandas as pd
from common import *
from words import WORDS, REGIONAL

R = jload(f"{DATA}/results.json")
A = pd.read_csv(f"{DATA}/alleys.csv", keep_default_na=False)
Wd = R["words"]
# facts stated in words
assert Wd["chare"]["home_pc"] == 100 and Wd["shut"]["home_pc"] == 100 and Wd["shut"]["top_town"] == "Shrewsbury" and Wd["shut"]["top_town_n"] == 3
assert [t["town"] for t in R["word_town"]["twitten"][:3]] == ["Haywards Heath", "Burgess Hill", "Lewes"]
assert R["word_town"]["ope"][0]["town"] == "Plymouth" and {"Truro", "Falmouth"} <= {t["town"] for t in R["word_town"]["ope"]}
assert ((A.word == "ope") & (A.town == "Portland")).sum() == 3
assert R["word_town"]["loke"][0]["town"] == "North Walsham" and R["word_town"]["chare"][0]["town"] == "Newcastle upon Tyne"
assert ((A.word == "jitty") & (A.town == "Loughborough")).sum() == 4 and ((A.word == "jitty") & A.town.isin(["Madeley", "Broseley"])).sum() >= 3
assert 30 <= Wd["ginnel"]["top_county_pc"] <= 36 and Wd["ginnel"]["top_county"] == "West Yorkshire"
assert Wd["lonnen"]["home_pc"] > 90
assert not (A.word == "jigger").any() and (A.word == "tenfoot").sum() == 1 and A[A.word == "tenfoot"].town.iloc[0] == "Hessle"
assert not ((A.word == "gully") & (A.town == "Birmingham")).any() and Wd["gully"]["top_town"] == "Bristol"
assert Wd["gully"]["n"] == 6 and Wd["gully"]["top_town_n"] == 3                      # "half of the six ... in Bristol"
assert 2 * R["wharfedale"]["snicket"] > R["yorks"]["snicket"]                          # "most of Yorkshire's named snickets"
assert ((A.word == "ope") & (A.town == "Saltash")).sum() == 1                           # paper: one Plymouth ope counted to Saltash
assert {"Truro", "Falmouth"} <= set(A[(A.word == "ope") & (A.town != "Plymouth")].town)  # blog: rest in Truro, Falmouth, Portland
assert R["towns_all"][0]["town"] == "London" and R["towns_all"][1]["town"] == "Edinburgh" and R["towns_all"][2]["town"] == "Hastings"
assert R["towns_regional"][0]["town"] == "Edinburgh" and R["towns_most_words"][0]["town"] == "Edinburgh"
assert [t["town"] for t in R["towns_regional"][1:5]] == ["Kirkcaldy", "Dundee", "Elgin", "Aberdeen"], R["towns_regional"][:5]
assert R["words"]["close"]["top_county"] == "City of Edinburgh" and R["word_town"]["close"][1]["town"] == "Elgin"
assert {"Leeds", "Huddersfield", "Harrogate", "Skipton"} <= set(R["yorks"]["ginnel_towns"]) and set(R["yorks"]["snicket_towns"]) == {"Ilkley", "Otley"}
assert R["wharfedale"]["nearest_ginnel_town"] == "Yeadon"
assert R["york"]["snicket"] == 0 and R["wharfedale"]["snicket"] >= 7
assert max(R["hex"]["dominant"], key=R["hex"]["dominant"].get) == "wynd"
CH = '<button class="chip" data-w="all" aria-pressed="true">All</button>' + "".join(
    f'<button class="chip" data-w="{k}" aria-pressed="false">{k}</button>' for k, *_ in WORDS if k in REGIONAL and Wd.get(k, {}).get("n", 0) >= 6)
t = open(os.path.join(ROOT, "code", "page_template.html"), encoding="utf-8").read()
css = open(os.path.join(ROOT, "code", "page.css"), encoding="utf-8").read()
fs = open(os.path.join(ROOT, "code", "fullscreen_snippet.html"), encoding="utf-8").read()
t = t.replace("{{CSS}}", css).replace("{{CHIPS}}", CH).replace("{{FULLSCREEN}}", fs)
t = t.replace("{{BYLINE}}", BYLINE).replace("{{AI}}", AI).replace("{{VERSION}}", time.strftime("%Y%m%d")).replace("{{REPO}}", REPO)
t = fill(t, R)
assert set(re.findall(r"\{\{([^}]+)\}\}", t)) <= {"DOI", "DOI_URL", "BLOG_URL"}, set(re.findall(r"\{\{([^}]+)\}\}", t))
vis = re.sub(r"<script.*?</script>|<style.*?</style>|<!--.*?-->", "", t, flags=re.S)
for bad in ("—", "–", "--", "DSIT", "DCMS", "civil serv"):
    assert bad not in vis, bad
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(t)
js = open(os.path.join(ROOT, "js", "page.js"), encoding="utf-8").read()
assert "—" not in js and "–" not in js
print("index.html", len(t) // 1024, "KB")
