#!/usr/bin/env python3
"""Add LocalBusiness (ProfessionalService) + WebSite nodes to the home @graph.
Honest fields only (service-area business: no invented street/phone). Fills the
LocalBusiness:0 / WebSite:0 gap — a first-order local-SEO + answer-engine signal
for a Kyiv B2B coffee-service. Idempotent: skips nodes already present. Parses the
ld+json as JSON (no regex surgery on the payload)."""
import re, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://aeo.animacoffee.com.ua"

def patch(path, lang_default="en"):
    p = ROOT / path
    if not p.exists(): return f"skip {path} (absent)"
    h = p.read_text(encoding="utf-8")
    m = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)', h, re.S)
    if not m: return f"skip {path} (no ld+json)"
    try:
        data = json.loads(m.group(2))
    except Exception as e:
        return f"skip {path} (unparseable: {e})"
    if not isinstance(data, dict) or "@graph" not in data:
        return f"skip {path} (no @graph)"
    graph = data["@graph"]
    have = {n.get("@type") for n in graph if isinstance(n, dict)}
    added = []
    if "LocalBusiness" not in have and "ProfessionalService" not in have:
        graph.append({
            "@type": "ProfessionalService",
            "@id": f"{BASE}/#localbusiness",
            "name": "Anima Volitiva",
            "url": BASE + "/",
            "image": f"{BASE}/assets/hero.jpg",
            "description": ("Full-service B2B coffee programs for offices, HoReCa and retail "
                            "across Kyiv & Kyiv Oblast — Swiss super-automatic machines, "
                            "specialty beans, 24/7 support and a flat monthly invoice."),
            "areaServed": [
                {"@type": "City", "name": "Kyiv"},
                {"@type": "State", "name": "Kyiv Oblast"}
            ],
            "address": {
                "@type": "PostalAddress",
                "addressLocality": "Kyiv",
                "addressRegion": "Kyiv Oblast",
                "addressCountry": "UA"
            },
            "priceRange": "$$$",
            "currenciesAccepted": "UAH",
            "knowsLanguage": ["uk", "en"],
            "serviceType": ["Coffee machine rental", "Specialty bean supply",
                            "Equipment maintenance", "Barista training"],
            "parentOrganization": {"@id": f"{BASE}/#organization"},
            "sameAs": []
        })
        added.append("ProfessionalService")
    if "WebSite" not in have:
        graph.append({
            "@type": "WebSite",
            "@id": f"{BASE}/#website",
            "url": BASE + "/",
            "name": "Anima Volitiva",
            "inLanguage": ["en", "uk"],
            "publisher": {"@id": f"{BASE}/#organization"}
        })
        added.append("WebSite")
    if not added:
        return f"ok  {path} (already had LocalBusiness+WebSite)"
    new_ld = m.group(1) + json.dumps(data, ensure_ascii=False, indent=2) + m.group(3)
    h = h[:m.start()] + new_ld + h[m.end():]
    p.write_text(h, encoding="utf-8")
    return f"ADD {path}: {', '.join(added)}"

for pg in ["index.html", "ua/index.html"]:
    print(patch(pg))
