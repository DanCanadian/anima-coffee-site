#!/usr/bin/env python3
"""Regenerate sitemap.xml from actual on-disk pages. Compounding: every render
re-runs this so new landings can never fall out of the sitemap again.
EN root + answers/ + UA mirror. PPC is noindex -> excluded (has ppc-sitemap.xml).
Usage: python3 tools/gen_sitemap.py [--base https://aeo.animacoffee.com.ua] [--date YYYY-MM-DD]
"""
import argparse, pathlib, datetime

ap = argparse.ArgumentParser()
ap.add_argument("--base", default="https://aeo.animacoffee.com.ua")
ap.add_argument("--date", default=datetime.date.today().isoformat())
a = ap.parse_args()
root = pathlib.Path(__file__).resolve().parent.parent
BASE, DATE = a.base.rstrip("/"), a.date

def url_for(p: pathlib.Path) -> str:
    rel = p.relative_to(root).as_posix()
    if rel == "index.html": return "/"
    if rel == "ua/index.html": return "/ua/"
    return "/" + rel

def _indexable(p):
    # skip pages carrying a robots noindex directive (thin tier stays live but out of sitemap)
    try:
        return 'noindex' not in p.read_text(encoding='utf-8', errors='ignore').lower()
    except Exception:
        return True

def collect(globpat):
    return sorted(p for p in root.glob(globpat)
                  if "ppc/" not in p.as_posix() and _indexable(p))

en = collect("*.html") + collect("answers/*.html") + collect("blog/*.html")
ua = collect("ua/*.html") + collect("ua/answers/*.html") + collect("ua/blog/*.html")

def ua_counterpart(en_path):
    rel = en_path.relative_to(root).as_posix()
    cand = root / "ua" / rel
    return cand if cand.exists() else None

rows = []
def emit(loc, alt_uk=None, alt_en=None):
    s = f'  <url>\n    <loc>{BASE}{loc}</loc><lastmod>{DATE}</lastmod>\n    <changefreq>weekly</changefreq>\n'
    if alt_uk:
        s += f'    <xhtml:link rel="alternate" hreflang="uk" href="{BASE}{alt_uk}"/>\n'
        s += f'    <xhtml:link rel="alternate" hreflang="en" href="{BASE}{alt_en}"/>\n'
        s += f'    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}{alt_en}"/>\n'
    s += "  </url>"
    rows.append(s)

for p in en:
    loc = url_for(p)
    uc = ua_counterpart(p)
    emit(loc, url_for(uc) if uc else None, loc if uc else None)
for p in ua:
    emit(url_for(p))

out = ('<?xml version="1.0" encoding="UTF-8"?>\n'
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
       'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
       + "\n".join(rows) + "\n</urlset>\n")
(root / "sitemap.xml").write_text(out, encoding="utf-8")
print(f"sitemap.xml: {len(en)} EN + {len(ua)} UA = {len(en)+len(ua)} <loc>")
