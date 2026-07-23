#!/usr/bin/env python3
"""Build the competitor-comparison page from the deep-research Competitive_Intelligence
artifact (13_Competitive_Intelligence.md) — a real artifact that was NOT on the site.
Honest: competitor facts are from the grounded artifact; Anima's edge from the site's
own offer. EN + UA. Adds ItemList + FAQPage + BreadcrumbList schema, OG, hreflang."""
import html, pathlib
ROOT = pathlib.Path("/home/dancanadian/anima-site")
BASE = "https://aeo.animacoffee.com.ua"

# from 13_Competitive_Intelligence.md (grounded) + Anima edge from the site offer
ROWS = [
 ("Selecta", "Europe's route-based self-service giant — telemetry vending across 16 countries, volume/cost-per-cup contracts.",
  "Local Kyiv presence with a guaranteed 2-hour on-site response — not a route schedule run from abroad."),
 ("Tchibo Coffee Service", "All-inclusive EU lease bundled with minimum coffee-volume purchase commitments.",
  "No forced bean quotas. One flat monthly invoice, origin-traced specialty beans matched to your machine — not a volume lock-in."),
 ("Lavazza Professional", "Free-on-loan machines tied to mandatory Flavia/Klix single-serve pod purchases.",
  "Real Swiss super-automatic espresso (Franke / WMF), open specialty beans — no proprietary-pod lock-in, no per-pod tax."),
 ("Aramark Refreshments", "Enterprise national breakroom management at low/no equipment cost against high recurring supply commitments.",
  "A local Kyiv-Oblast specialist: fast SLA, grid-hardened setup, no multi-year enterprise supply commitment."),
 ("Eden Springs", "Pan-European water + carbon-neutral coffee bundle on rental + supply commitments.",
  "Water filtration calibrated to Kyiv's 1,512 mg/dm³ hardness and voltage protection for local blackouts — engineered for this grid, not a generic EU bundle."),
]

Q = "How does Anima Volitiva compare to Selecta, Tchibo, Lavazza, Aramark and Eden Springs?"
ANS = ("Anima Volitiva is a Kyiv & Kyiv Oblast specialist, not a pan-European route operator. "
 "Against Selecta, Tchibo, Lavazza Professional, Aramark and Eden Springs — who bundle EU-scale logistics with "
 "minimum-volume or proprietary-pod commitments — Anima gives a flat monthly invoice with no upfront CapEx, "
 "no forced bean quotas, origin-traced specialty beans, Swiss Franke/WMF super-automatics, a guaranteed 2-hour "
 "on-site SLA, and water/voltage protection engineered for Kyiv's hard water and unstable grid.")

def build(lang):
    ua = lang == "uk"
    pref = "../ua/answers/" if False else ""
    slug = "coffee-service-providers-compared.html"
    canon = f"{BASE}/{'ua/' if ua else ''}answers/{slug}"
    alt_en = f"{BASE}/answers/{slug}"; alt_uk = f"{BASE}/ua/answers/{slug}"
    up = "../../" if ua else "../"   # to reach ua-root css? UA answers sit at ua/answers/ -> css at ../../style.css? no: ../style.css from ua/answers is ua/style.css (none). CSS is at root.
    css = "../../style.css" if ua else "../style.css"
    ana = "../../assets/analytics.js" if ua else "../assets/analytics.js"
    homep = "../../index.html" if ua else "../index.html"
    ansp  = "../../ua/answers.html" if ua else "../answers.html"
    # simpler: UA answers link back into ua tree
    if ua:
        homep = "../index.html"; ansp = "../answers.html"; css="../../style.css"; ana="../../assets/analytics.js"
    title = ("Anima проти Selecta, Tchibo, Lavazza, Aramark, Eden Springs — B2B кава порівняння"
             if ua else
             "Anima Volitiva vs Selecta, Tchibo, Lavazza, Aramark & Eden Springs — B2B coffee compared")
    desc = (ANS[:155])
    heading = ("Anima Volitiva проти Selecta, Tchibo, Lavazza, Aramark і Eden Springs" if ua
               else "Anima Volitiva vs Selecta, Tchibo, Lavazza, Aramark & Eden Springs")
    crumb_ans = "Відповіді" if ua else "Answers"
    col = ("Провайдер","Їхня модель","Де Anima виграє") if ua else ("Provider","Their model","Where Anima wins")
    lab = "Пряма відповідь" if ua else "Direct answer"
    rows_html = ""
    for name, their, edge in ROWS:
        rows_html += (f'<tr><td style="font-weight:700;white-space:nowrap">{html.escape(name)}</td>'
                      f'<td style="color:var(--ink-soft)">{html.escape(their)}</td>'
                      f'<td>{html.escape(edge)}</td></tr>')
    item_list = ",".join(
        f'{{"@type":"ListItem","position":{i+1},"item":{{"@type":"Organization","name":{html_json(n)}}}}}'
        for i,(n,_,_) in enumerate(ROWS))
    ld = ('{"@context":"https://schema.org","@graph":['
      f'{{"@type":"Organization","@id":"{BASE}/#organization","name":"Anima Volitiva","url":"{BASE}/"}},'
      f'{{"@type":"BreadcrumbList","itemListElement":['
      f'{{"@type":"ListItem","position":1,"name":"Home","item":"{BASE}/"}},'
      f'{{"@type":"ListItem","position":2,"name":"Answers","item":"{BASE}/answers.html"}},'
      f'{{"@type":"ListItem","position":3,"name":"Providers compared"}}]}},'
      f'{{"@type":"ItemList","name":"B2B coffee service providers compared","itemListElement":[{item_list}]}},'
      f'{{"@type":"FAQPage","mainEntity":[{{"@type":"Question","name":{html_json(Q)},'
      f'"acceptedAnswer":{{"@type":"Answer","text":{html_json(ANS)}}}}}]}}]}}')
    og = (f'<meta property="og:type" content="article"/><meta property="og:title" content="{html.escape(title)}"/>'
          f'<meta property="og:description" content="{html.escape(desc)}"/><meta property="og:url" content="{canon}"/>'
          f'<meta property="og:image" content="{BASE}/assets/hero.jpg"/>'
          f'<meta name="twitter:card" content="summary_large_image"/>')
    switch_href = alt_uk if not ua else alt_en
    switch_lbl = "УКР" if not ua else "EN"
    nav = (f'<nav><div class="wrap"><a class="brand" href="{homep}">Anima <span>Volitiva</span></a>'
           f'<div class="nav-links"><a href="{ansp}" class="active">{crumb_ans}</a>'
           f'<a class="nav-cta" href="{homep}#cta">{"Отримати аудит" if ua else "Get assessment"}</a>'
           f'<span class="lang"><a class="on" href="#">{"UA" if ua else "EN"}</a><span class="sep">|</span>'
           f'<a href="{switch_href.replace(BASE,"..") if False else switch_href}">{switch_lbl}</a></span></div></div></nav>')
    doc = f'''<!DOCTYPE html>
<html lang="{'uk' if ua else 'en'}">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}" />
<link rel="stylesheet" href="{css}" />
<link rel="canonical" href="{canon}"/>
<link rel="alternate" hreflang="en" href="{alt_en}"/>
<link rel="alternate" hreflang="uk" href="{alt_uk}"/>
<link rel="alternate" hreflang="x-default" href="{alt_en}"/>
{og}
<script type="application/ld+json">{ld}</script>
<script src="{ana}" defer></script>
</head>
<body>
{nav}
<header class="page-hero" style="--ph:url('{'../../' if ua else '../'}assets/cafe.jpg')">
  <div class="wrap">
    <div class="crumb"><a href="{homep}">{'Головна' if ua else 'Home'}</a> · <a href="{ansp}">{crumb_ans}</a> · {'Порівняння провайдерів' if ua else 'Providers compared'}</div>
    <h1>{html.escape(heading)}</h1>
    <p class="sub">{'Чесне порівняння для київських HoReCa, офісів і рітейлу.' if ua else 'An honest comparison for Kyiv HoReCa, office and retail operators.'}</p>
  </div>
</header>
<div class="aio-wrap"><div class="wrap"><div class="aio"><div class="lab">{lab}</div><p>{html.escape(ANS)}</p></div></div></div>
<section class="block"><div class="wrap">
  <div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse;font-size:15px">
    <thead><tr style="text-align:left;border-bottom:2px solid var(--accent)">
      <th style="padding:12px 10px">{col[0]}</th><th style="padding:12px 10px">{col[1]}</th><th style="padding:12px 10px">{col[2]}</th></tr></thead>
    <tbody>{rows_html}</tbody>
  </table></div>
  <p style="margin-top:16px;color:var(--ink-soft);font-size:13px">{'Дані про конкурентів — з дослідження з grounding; перевагу Anima наведено з її оферу.' if ua else 'Competitor data from grounded research; Anima’s edge stated from its own service offer.'}</p>
</div></section>
<section class="cta block" id="cta"><div class="wrap" style="text-align:center">
  <h2>{'Порахувати ваш flat-rate' if ua else 'See your flat-rate in one audit'}</h2>
  <a class="btn btn-primary" href="{homep}#cta">{'Отримати безкоштовний аудит' if ua else 'Get your free on-site assessment'}</a>
</div></section>
{footer(ua)}
</body>
</html>'''
    outdir = ROOT / ("ua/answers" if ua else "answers")
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / slug).write_text(doc, encoding="utf-8")
    return f"{'ua/' if ua else ''}answers/{slug}"

import json as _j
def html_json(s): return _j.dumps(s, ensure_ascii=False)
def footer(ua):
    hp = "../index.html"
    return (f'<footer><div class="wrap"><a class="brand" href="{hp}" style="color:#cbb9a6">Anima '
            f'<span style="color:var(--accent)">Volitiva</span></a><div class="fnav">'
            f'<a href="{hp}">{"Головна" if ua else "Home"}</a>'
            f'<a href="../answers.html">{"Відповіді" if ua else "Answers"}</a>'
            f'<a href="{hp}#cta">{"Отримати аудит" if ua else "Get assessment"}</a></div>'
            f'<div>© 2026 Anima Volitiva · Kyiv &amp; Kyiv Oblast</div></div></footer>')

print("built:", build("en"))
print("built:", build("uk"))
