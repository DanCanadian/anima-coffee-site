#!/usr/bin/env python3
"""Inject Open Graph + Twitter Card meta into every landing/answer page (EN + UA).
The whole OG layer was missing site-wide -> no share preview on Telegram/Slack/
LinkedIn and no card for link-unfurling answer surfaces. Sources are honest:
og:title from <title>, og:description from the existing meta description, og:url
from the existing canonical. Image = hero.jpg (1600x1067). Idempotent (skips pages
that already carry og:image). Re-runnable so new pages get cards automatically."""
import re, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://aeo.animacoffee.com.ua"
IMG  = f"{BASE}/assets/hero.jpg"

def og(path):
    p = ROOT / path
    t = p.read_text(encoding="utf-8", errors="ignore")
    if re.search(r'property="og:image"', t):
        return None  # already done
    title = re.search(r"<title>([^<]+)</title>", t)
    title = html.unescape(title.group(1).strip()) if title else "Anima Volitiva"
    desc = re.search(r'<meta name="description" content="([^"]*)"', t)
    desc = desc.group(1) if desc else ""
    canon = re.search(r'<link rel="canonical" href="([^"]+)"', t)
    url = canon.group(1) if canon else BASE + "/"
    is_ua = path.startswith("ua/")
    locale = "uk_UA" if is_ua else "en_US"
    alt = "en_US" if is_ua else "uk_UA"
    otype = "article" if "/answers/" in path else "website"
    tags = (
        f'\n<meta property="og:type" content="{otype}"/>'
        f'\n<meta property="og:site_name" content="Anima Volitiva"/>'
        f'\n<meta property="og:title" content="{html.escape(title)}"/>'
        f'\n<meta property="og:description" content="{html.escape(desc)}"/>'
        f'\n<meta property="og:url" content="{url}"/>'
        f'\n<meta property="og:image" content="{IMG}"/>'
        f'\n<meta property="og:image:width" content="1600"/>'
        f'\n<meta property="og:image:height" content="1067"/>'
        f'\n<meta property="og:locale" content="{locale}"/>'
        f'\n<meta property="og:locale:alternate" content="{alt}"/>'
        f'\n<meta name="twitter:card" content="summary_large_image"/>'
        f'\n<meta name="twitter:title" content="{html.escape(title)}"/>'
        f'\n<meta name="twitter:description" content="{html.escape(desc)}"/>'
        f'\n<meta name="twitter:image" content="{IMG}"/>\n'
    )
    # insert right after the canonical link if present, else after <title>
    if canon:
        i = t.index(canon.group(0)) + len(canon.group(0))
    else:
        mt = re.search(r"</title>", t); i = mt.end() if mt else t.index("<head>") + 6
    p.write_text(t[:i] + tags + t[i:], encoding="utf-8")
    return path

def collect():
    out = []
    for sub in ("", "ua/"):
        base = ROOT / sub if sub else ROOT
        for pat in ("*.html", "answers/*.html"):
            for q in sorted(base.glob(pat)):
                if "ppc/" in q.as_posix() or q.name == "sitemap.html": continue
                out.append(q.relative_to(ROOT).as_posix())
    return out

done = [og(p) for p in collect()]
done = [d for d in done if d]
print(f"OG/Twitter cards added to {len(done)} pages")
