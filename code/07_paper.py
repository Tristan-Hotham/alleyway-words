"""Step 7: the paper. Fills code/paper_template.tex from data/results.json, adds the word table, compiles with xelatex.
Output: release/paper/Hotham_Alleyway_Words.pdf and .tex beside the f_*.png figures.
The DOI stays a placeholder (https://doi.org/10.5281/zenodo.24086513 printed) unless DOI is set: DOI=10.5281/zenodo.N python3 code/07_paper.py"""
import subprocess
from common import *
from words import WORDS

R = jload(f"{DATA}/results.json")
OUT = os.path.join(ROOT, "release", "paper"); NAME = "Hotham_Alleyway_Words"
tex = lambda s: str(s).replace("\\", "").replace("&", "\\&").replace("%", "\\%").replace("_", "\\_").replace("#", "\\#").replace("$", "\\$")


def tfmt(v, f):
    if f == "int": return f"{int(round(float(v))):,}"
    if f == "pc": return f"{round(float(v))}\\%"
    if f == "f1": return f"{float(v):.1f}"
    if f == "f2": return f"{float(v):.2f}"
    return tex(str(v))


rows = ""
for k, lab, sp, col, kind, note in WORDS:
    w = R["words"].get(k)
    if not w:
        rows += f"{tex(lab)} & {tex(', '.join(sp))} & {tex(note)} & 0 & & \\\\\n"; continue
    top = f"{tex(w['top_county'])} ({w['top_county_pc']:.0f}\\%)"
    rows += f"{tex(lab)} & {tex(', '.join(sp))} & {tex(note)} & {w['n']:,} & {w['path_pc']:.0f} & {top}\\\\\n"
TW = ("\\begin{small}\\begin{longtable}{p{2.0cm}p{2.9cm}p{4.1cm}rrp{3.1cm}}\\caption{The alley words: spellings counted, the region where the word is "
      "usually reported (context, not a result), named alleys in the data, share that are footpaths (\\%), and the county with most.}\\label{tab:words}\\\\"
      "\\toprule Word & Spellings & Usually & Alleys & Path & Top county\\\\\\midrule\\endhead\n" + rows + "\\bottomrule\\end{longtable}\\end{small}")
t = open(os.path.join(ROOT, "code", "paper_template.tex"), encoding="utf-8").read()
t = t.replace("{{AI}}", AI).replace("{{TABLE_WORDS}}", TW)
t = re.sub(r"\{\{(?!TABLE_|DOI)([^}|]+)(\|(\w+))?\}\}", lambda m: tfmt(get(R, m.group(1)), m.group(3) or "raw"), t)
DOI = os.environ.get("DOI")
t = t.replace("https://doi.org/10.5281/zenodo.24086513", f"\\url{{https://doi.org/{DOI}}}" if DOI else "\\{\\{DOI\\_URL\\}\\}")
assert "{{" not in t and "--" not in t and "—" not in t and "–" not in t
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, NAME + ".tex"), "w", encoding="utf-8").write(t)
for _ in range(2):
    r = subprocess.run(["xelatex", "-interaction=nonstopmode", NAME + ".tex"], cwd=OUT, capture_output=True, text=True)
log = open(os.path.join(OUT, NAME + ".log"), encoding="utf-8", errors="ignore").read()
print([l for l in log.splitlines() if "Missing character" in l or "undefined" in l.lower() or "Overfull" in l][:12])
for ext in (".aux", ".log", ".out", ".bbl", ".blg"):
    q = os.path.join(OUT, NAME + ext)
    if os.path.exists(q): os.remove(q)
txt = subprocess.run(["pdftotext", os.path.join(OUT, NAME + ".pdf"), "-"], capture_output=True, text=True).stdout
pages = subprocess.run(["pdfinfo", os.path.join(OUT, NAME + ".pdf")], capture_output=True, text=True).stdout
print("paper", r.returncode, len(txt.split()), "words;", [l for l in pages.splitlines() if l.startswith("Pages")], "dashes:", txt.count("—") + txt.count("–") + txt.count("--"))
