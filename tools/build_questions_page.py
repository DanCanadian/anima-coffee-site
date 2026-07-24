#!/usr/bin/env python3
"""Wire the Customer_Question_Mining artifact (8_Customer_Question_Mining.md, 3768w) into a
real AEO page: top mined buyer-questions (by frequency) with grounded answers + the artifact's
Kyiv-Oblast pain-point summary. Answers are authored from the site's established offer facts
(2h SLA, flat monthly invoice, Franke/WMF, Kyiv water 15-20 dH, no bean quotas). EN + UA.
FAQPage + Article schema, OG, hreflang. Closes surface-artifact coverage 10/13 -> 11/13."""
import html, pathlib, json
ROOT = pathlib.Path("/home/dancanadian/anima-site")
BASE = "https://aeo.animacoffee.com.ua"
SLUG = "what-kyiv-coffee-operators-ask.html"

# top mined questions (from the artifact's Top-30 inventory, freq >=8) with grounded answers
QA = [
 ("How do I choose between renting a Swiss super-automatic (Franke/WMF) or buying one outright for a 50-person Kyiv office?",
  "Buying ties up $3,500–$15,000+ per unit in depreciating hardware and leaves you owning every repair, scale failure and downtime day. Renting under Anima’s flat monthly invoice keeps that capital free: you get the same Franke/WMF machine, sized in a free on-site audit, plus beans, staff training, water/voltage protection and a 2-hour on-site SLA — one predictable OpEx line, no CapEx."),
 ("If our gas station in Kyiv Oblast breaks down on a Sunday, how fast can a certified technician arrive with parts?",
  "Anima guarantees a 2-hour on-site response across Kyiv & Kyiv Oblast, 24/7 — weekends included — with certified technicians carrying diagnostic tools and proprietary Swiss parts. For a forecourt where downtime is direct lost sales (up to ~$500/day), that SLA is the difference between a coffee outage and uninterrupted revenue."),
 ("How does hard Kyiv municipal water affect professional WMF/Franke boilers over six months?",
  "Kyiv-region water runs 15–20 dH. Without active filtration and scheduled scale calibration, that mineral load causes catastrophic boiler scaling in 6–12 months. Anima installs filtration calibrated to your local hardness and runs preventive descaling, so the boiler never reaches failure — the scaling risk is engineered out, not billed later."),
 ("Can we rent a professional Swiss machine for a Kyiv retail showroom without a long-term minimum contract?",
  "Yes. There is no forced minimum term and no mandatory bean-volume quota. You pay one flat monthly fee that already includes the machine, specialty beans, service and support — so you scale up or down without being locked into a multi-year lease or a consumables commitment."),
 ("What is included in the mandatory staff barista training, and how does it prevent breakdowns?",
  "Every deployment includes a mandatory 2-hour barista onboarding covering correct grind, milk-system hygiene and daily care. In high-turnover HoReCa and retail, untrained staff are the top cause of milk blockages and avoidable failures — the training halts that quality drift and cuts complaints, and it’s covered by the flat invoice, not an add-on."),
 ("How does a single monthly OPEX invoice actually cover maintenance, training, beans and rental together?",
  "Anima’s zero-headache model bundles hardware rental, origin-traced specialty beans, mandatory training, water/voltage protection and 24/7 technical support with a 2-hour SLA into one flat monthly figure. Technical labour and parts are inside the fee — there are no surprise repair bills, which is the single most common misconception buyers arrive with."),
 ("Why does our office coffee taste increasingly bitter even though we use premium beans and never touched the grinder?",
  "Bitterness that creeps in without a settings change is almost always scale and calibration drift — hardened boilers and an un-recalibrated grind pull over-extracted, bitter shots. Anima’s monthly calibration re-syncs grind, pressure and temperature to your specific beans and water, restoring a consistent cup without you changing anything."),
 ("If high staff turnover means untrained employees damage the machine, who pays for the repair?",
  "Under Anima’s managed model, technical repairs and parts are inside the flat monthly fee — you are not hit with a surprise bill when a new hire causes a fault. Combined with the mandatory training that prevents most damage in the first place, the risk of turnover-driven repair costs is removed from your P&L."),
 ("Why is our self-managed coffee program underperforming versus outsourcing to a managed service at our retail location?",
  "Self-managed programs quietly leak revenue to downtime, scale failures, inconsistent quality and staff error. A managed service with a 2-hour SLA, calibrated specialty beans and trained staff keeps the machine producing sellable, consistent coffee — retail operators on the calibrated model see materially higher coffee-related revenue than commodity self-service setups."),
 ("Why are our rental costs fluctuating monthly when we were promised a fixed-price contract?",
  "Fluctuating invoices usually mean your current vendor treats service calls, parts or bean volume as variable add-ons. Anima’s contract is a genuine flat monthly rate — machine, beans, service and support are all inside one fixed figure, so the number you sign is the number you pay every month."),
]

def pains():
    d = json.load(open("/tmp/qmining.json"))
    out = []
    for h, b in d.get("pains", []):
        h = h.strip()
        if h.lower() == "question" or len(h) > 60: continue
        out.append((h, b.strip()))
        if len(out) >= 5: break
    return out

def build(ua):
    canon = f"{BASE}/{'ua/' if ua else ''}answers/{SLUG}"
    alt_en, alt_uk = f"{BASE}/answers/{SLUG}", f"{BASE}/ua/answers/{SLUG}"
    css = "../../style.css" if ua else "../style.css"
    ana = "../../assets/analytics.js" if ua else "../assets/analytics.js"
    heroimg = ("../../" if ua else "../") + "assets/cafe.jpg"
    homep = "../index.html"; ansp = "../answers.html"
    title = ("Що питають київські оператори кави — реальні відповіді" if ua
             else "What Kyiv coffee operators actually ask — grounded answers")
    intro = ("Реальні високочастотні питання B2B-покупців Києва та області — з прямими відповідями для людей і answer-рушіїв."
             if ua else
             "The real, high-frequency questions Kyiv & Oblast B2B buyers ask — with direct, citable answers for people and answer engines.")
    lab = "Пряма відповідь" if ua else "Direct answer"
    faq_html = ""
    for q, a in QA:
        faq_html += (f'<details class="qa" style="border-bottom:1px solid var(--line);padding:16px 0">'
                     f'<summary style="font-weight:700;font-size:17px;cursor:pointer">{html.escape(q)}</summary>'
                     f'<p style="margin:12px 0 0;color:var(--ink-soft);line-height:1.7">{html.escape(a)}</p></details>')
    pain_html = "".join(
        f'<li style="margin-bottom:10px"><b>{html.escape(h)}.</b> <span style="color:var(--ink-soft)">{html.escape(b)}</span></li>'
        for h, b in pains())
    faq_ld = ",".join(
        f'{{"@type":"Question","name":{json.dumps(q,ensure_ascii=False)},"acceptedAnswer":{{"@type":"Answer","text":{json.dumps(a,ensure_ascii=False)}}}}}'
        for q, a in QA)
    ld = ('{"@context":"https://schema.org","@graph":['
          f'{{"@type":"Organization","@id":"{BASE}/#organization","name":"Anima Volitiva","url":"{BASE}/"}},'
          f'{{"@type":"BreadcrumbList","itemListElement":['
          f'{{"@type":"ListItem","position":1,"name":"Home","item":"{BASE}/"}},'
          f'{{"@type":"ListItem","position":2,"name":"Answers","item":"{BASE}/answers.html"}},'
          f'{{"@type":"ListItem","position":3,"name":"What operators ask"}}]}},'
          f'{{"@type":"FAQPage","mainEntity":[{faq_ld}]}}]}}')
    switch = alt_uk if not ua else alt_en
    nav = (f'<nav><div class="wrap"><a class="brand" href="{homep}">Anima <span>Volitiva</span></a>'
           f'<div class="nav-links"><a href="{ansp}" class="active">{"Відповіді" if ua else "Answers"}</a>'
           f'<a class="nav-cta" href="{homep}#cta">{"Отримати аудит" if ua else "Get assessment"}</a>'
           f'<span class="lang"><a class="on" href="#">{"UA" if ua else "EN"}</a><span class="sep">|</span>'
           f'<a href="{switch}">{"EN" if ua else "УКР"}</a></span></div></div></nav>')
    footer = (f'<footer><div class="wrap"><a class="brand" href="{homep}" style="color:#cbb9a6">Anima '
              f'<span style="color:var(--accent)">Volitiva</span></a><div class="fnav">'
              f'<a href="{homep}">{"Головна" if ua else "Home"}</a><a href="{ansp}">{"Відповіді" if ua else "Answers"}</a>'
              f'<a href="{homep}#cta">{"Отримати аудит" if ua else "Get assessment"}</a></div>'
              f'<div>© 2026 Anima Volitiva · Kyiv &amp; Kyiv Oblast</div></div></footer>')
    doc = f'''<!DOCTYPE html>
<html lang="{'uk' if ua else 'en'}">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(intro[:155])}" />
<link rel="stylesheet" href="{css}" />
<link rel="canonical" href="{canon}"/>
<link rel="alternate" hreflang="en" href="{alt_en}"/>
<link rel="alternate" hreflang="uk" href="{alt_uk}"/>
<link rel="alternate" hreflang="x-default" href="{alt_en}"/>
<meta property="og:type" content="article"/>
<meta property="og:title" content="{html.escape(title)}"/>
<meta property="og:description" content="{html.escape(intro[:155])}"/>
<meta property="og:url" content="{canon}"/>
<meta property="og:image" content="{BASE}/assets/hero.jpg"/>
<meta name="twitter:card" content="summary_large_image"/>
<script type="application/ld+json">{ld}</script>
<script src="{ana}" defer></script>
</head>
<body>
{nav}
<header class="page-hero" style="--ph:url('{heroimg}')"><div class="wrap">
  <div class="crumb"><a href="{homep}">{'Головна' if ua else 'Home'}</a> · <a href="{ansp}">{'Відповіді' if ua else 'Answers'}</a> · {'Що питають оператори' if ua else 'What operators ask'}</div>
  <h1>{html.escape(title)}</h1>
  <p class="sub">{html.escape(intro)}</p>
</div></header>
<div class="aio-wrap"><div class="wrap"><div class="aio"><div class="lab">{lab}</div><p>{html.escape(QA[0][1])}</p></div></div></div>
<section class="block"><div class="wrap" style="max-width:900px">
  <h2 style="font-size:24px;margin-bottom:8px">{'Головні болі операторів у Києві та області' if ua else 'Top pain points for Kyiv & Oblast operators'}</h2>
  <ul style="list-style:none;padding:0;margin:0 0 8px">{pain_html}</ul>
</div></section>
<section class="block"><div class="wrap" style="max-width:900px">
  <h2 style="font-size:24px;margin-bottom:8px">{'Питання, які реально ставлять' if ua else 'The questions operators actually ask'}</h2>
  {faq_html}
</div></section>
<section class="cta block" id="cta"><div class="wrap" style="text-align:center">
  <h2>{'Порахувати ваш flat-rate за один аудит' if ua else 'Get your flat-rate in one on-site audit'}</h2>
  <a class="btn btn-primary" href="{homep}#cta">{'Отримати безкоштовний аудит' if ua else 'Get your free assessment'}</a>
</div></section>
{footer}
</body></html>'''
    outdir = ROOT / ("ua/answers" if ua else "answers")
    (outdir / SLUG).write_text(doc, encoding="utf-8")
    return f"{'ua/' if ua else ''}answers/{SLUG}"

print("built:", build(False))
print("built:", build(True))
