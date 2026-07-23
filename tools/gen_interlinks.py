#!/usr/bin/env python3
"""Generate a topical internal-linking graph from the deep-research Topic Cluster Map
(16_Topic_Cluster_Map.json) and inject a "Related answers" block into every landing +
answer page. Compounding: idempotent (keyed on <!--interlink-graph-->), re-runnable so
new pages join the graph automatically. Internal linking is a first-order AEO/SEO lever;
this wires the cluster-map artifact that the run DID emit into real on-page structure.

EN pages link EN siblings; ua/ pages link ua/ siblings. Assignment = kg-entity token
overlap between each page's data-kg-ref set and each cluster's kg_entities.
Usage: python3 tools/gen_interlinks.py [--map PATH]
"""
import argparse, pathlib, re, json, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
ap = argparse.ArgumentParser()
ap.add_argument("--map", default=str(pathlib.Path.home() /
    "dev/adv-ai-hub/deep_research/output/Anima_Volitiva_20260619_025316_REAL_KG/16_Topic_Cluster_Map.json"))
a = ap.parse_args()

MARKER = "<!--interlink-graph-->"
STOP = {"the","a","an","and","or","for","in","of","to","how","what","why","is","vs",
        "&","/","-","2","24","7","2-hour","247","kyiv","oblast","coffee","machine","machines","service"}

def toks(s):
    return {t for t in re.split(r"[^a-z0-9]+", s.lower()) if t and t not in STOP and not t.isdigit()}

clusters = json.load(open(a.map, encoding="utf-8"))["clusters"]
CL = [(c["cluster_id"], c["pillar_title"], set().union(*[toks(e) for e in c.get("kg_entities", [])] or [set()]))
      for c in clusters]

def page_signal(p):
    t = p.read_text(encoding="utf-8", errors="ignore")
    kg = set(re.findall(r'data-kg-ref="([^"]+)"', t))
    kg.discard("None")
    title = re.search(r"<title>([^<]+)", t)
    title = html.unescape(title.group(1).split("|")[0].strip()) if title else p.stem
    sig = set().union(*[toks(k.replace("_", " ")) for k in kg] or [set()]) | toks(title)
    return title, kg, sig

def collect(subdir=""):
    base = ROOT / subdir if subdir else ROOT
    pages = []
    for pat in ("*.html", "answers/*.html"):
        for p in sorted(base.glob(pat)):
            if "ppc/" in p.as_posix(): continue
            if p.name in ("index.html", "sitemap.html"): continue
            pages.append(p)
    return pages

def build(subdir, heading, cta_word):
    pages = collect(subdir)
    if not pages: return 0
    meta = {}
    for p in pages:
        title, kg, sig = page_signal(p)
        # best cluster by token overlap
        best = max(CL, key=lambda c: len(sig & c[2]))
        meta[p] = {"title": title, "kg": kg, "sig": sig,
                   "cluster": best[0] if (sig & best[2]) else None}
    written = 0
    for p in pages:
        info = meta[p]
        # rank other pages: shared cluster first, then shared-kg count, then sig overlap
        def score(q):
            m = meta[q]
            s = 0
            if info["cluster"] and m["cluster"] == info["cluster"]: s += 100
            s += 10 * len(info["kg"] & m["kg"])
            s += len(info["sig"] & m["sig"])
            return s
        sibs = sorted((q for q in pages if q is not p), key=score, reverse=True)
        sibs = [q for q in sibs if score(q) > 0][:4]
        if len(sibs) < 3:  # top up so every page links out
            sibs = (sibs + [q for q in pages if q is not p and q not in sibs])[:4]
        items = ""
        for q in sibs:
            href = q.name if not subdir else q.relative_to(ROOT / subdir).as_posix()
            if q.parent.name == "answers":
                href = ("answers/" if not subdir else "answers/") + q.name
            items += (f'<li><a href="{href}" rel="related" '
                      f'style="color:var(--accent);text-decoration:none;font-weight:600">'
                      f'{html.escape(meta[q]["title"])}</a></li>')
        block = (f'\n{MARKER}\n<section class="block" aria-label="Related">'
                 f'<div class="wrap"><div class="center-head" style="text-align:left;margin-bottom:16px">'
                 f'<h2 style="font-size:24px">{heading}</h2></div>'
                 f'<ul class="value-list" style="line-height:2">{items}</ul></div></section>\n')
        t = p.read_text(encoding="utf-8", errors="ignore")
        # idempotent: strip prior graph block
        t = re.sub(re.escape(MARKER) + r'.*?</section>\s*', "", t, flags=re.S)
        # inject before CTA section, else before footer
        m = re.search(r'<section class="cta', t)
        idx = m.start() if m else t.find("<footer")
        if idx < 0: idx = t.rfind("</body>")
        t = t[:idx] + block + t[idx:]
        p.write_text(t, encoding="utf-8")
        written += 1
    return written

en = build("", "Related answers", "Related")
ua = build("ua", "Схожі відповіді", "Схожі")
print(f"interlink graph: {en} EN + {ua} UA pages wired from {len(CL)} clusters")
