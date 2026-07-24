#!/usr/bin/env python3
"""Wire the Brand_Blog_Post artifact into a real blog section (index + post, EN+UA) — the
last surface artifact (13/13). Long-form authority content for AEO. Article + BreadcrumbList
schema, OG, hreflang. EN prose from the artifact; UA = faithful native translation."""
import json, html, pathlib
ROOT = pathlib.Path("/home/dancanadian/anima-site")
BASE = "https://aeo.animacoffee.com.ua"
SLUG = "capex-vs-opex-b2b-coffee-kyiv.html"

d = json.load(open("/tmp/blog.json"))
EN = {
 "title": "CAPEX vs OPEX: structuring high-performance B2B coffee operations in Kyiv Oblast",
 "dek": "Why Kyiv operators are replacing $3,200–$16,000 upfront equipment purchases with a single flat monthly OPEX invoice.",
 "intro": d["intro"],
 "secs": d["secs"],
}
UA = {
 "title": "CAPEX проти OPEX: як будувати високопродуктивний B2B-кавовий сервіс у Києві та області",
 "dek": "Чому київські оператори замінюють закупівлю обладнання за $3 200–$16 000 на єдиний фіксований щомісячний OPEX-рахунок.",
 "intro": ("Комерційний кавовий бізнес у Києві та області одразу впирається в капітальний бар’єр: одна швейцарська "
   "суперавтоматична еспресо-система коштує наперед $3 200–$16 000. У 2026-му компанії системно відмовляються від "
   "прямої купівлі обладнання, щоб зберегти ліквідність. Дешеве некероване обладнання чи фрагментовані оренди "
   "ведуть до складності, непередбачуваних поломок і падіння якості.\n\nТрадиційні моделі в Україні зламані: один "
   "вендор здає машину, інший постачає зерно, третій ремонтує — а коли машина ламається, клієнт застрягає в колі "
   "перекладання відповідальності. Це простої та втрата високомаржинального доходу з кави.\n\nAnima Volitiva "
   "замінює цей ланцюг єдиним Zero-Headache рішенням: швейцарське обладнання, підібране спешелті-зерно, обов’язкове "
   "2-годинне навчання персоналу та цілодобова підтримка — в одному передбачуваному щомісячному OPEX-рахунку, без "
   "капітальних вкладень і без мінімального терміну контракту."),
 "secs": [
   ("Технічне калібрування та онбординг: усуваємо точки відмови київських кавових операцій",
    "Щоб якість напою була стабільною, обладнання треба ретельно калібрувати. Київська водопровідна вода жорстка й "
    "агресивна до суперавтоматів. Без правильного налаштування водолінії та профілактики накип і хибний тиск "
    "екстракції швидко руйнують машину. Anima Volitiva знімає ці ризики з першого дня: обстеження майданчика, "
    "професійна водопідготовка, тюнінг тиску та калібрування. Поєднуючи спешелті-зерно з оптимізованими "
    "швейцарськими машинами (Franke, WMF), ми гарантуємо стабільний профіль кави. Плюс обов’язкове 2-годинне "
    "навчання персоналу з кожною інсталяцією — воно прибирає найпоширеніші поломки через людський фактор."),
   ("2-годинний аварійний SLA: усуваємо простої та максимізуємо дохід",
    "Для рітейлу, АЗК і ресторанів зламана кавомашина — це прямий удар по денному P&L. Anima гарантує виїзд "
    "техніка на місце за 2 години по всьому Києву та області, цілодобово, із запчастинами та підмінним обладнанням. "
    "Один фіксований щомісячний рахунок покриває ремонт і сервіс — без раптових рахунків. Результат: нуль "
    "тривалих простоїв у пікові години та передбачувані витрати."),
 ],
}

def md_to_html(s):
    out = ""
    for para in s.split("\n\n"):
        p = html.escape(para.strip())
        p = p.replace("Anima Volitiva", "<strong>Anima Volitiva</strong>")
        if p: out += f'<p style="margin:0 0 18px;color:var(--ink-soft);line-height:1.8">{p}</p>'
    return out

def build_post(lang):
    c = UA if lang == "uk" else EN
    canon = f"{BASE}/{'ua/' if lang=='uk' else ''}blog/{SLUG}"
    alt_en, alt_uk = f"{BASE}/blog/{SLUG}", f"{BASE}/ua/blog/{SLUG}"
    up = "../../" if lang=="uk" else "../"
    css = up+"style.css"; ana = up+"assets/analytics.js"; home = "../index.html"; blog = "index.html"
    hero = up+"assets/cafe.jpg"
    secs_html = "".join(f'<h2 style="font-size:24px;margin:28px 0 12px">{html.escape(h)}</h2>{md_to_html(b)}'
                        for h, b in c["secs"])
    ld = ('{"@context":"https://schema.org","@graph":['
          f'{{"@type":"Organization","@id":"{BASE}/#organization","name":"Anima Volitiva","url":"{BASE}/"}},'
          f'{{"@type":"BreadcrumbList","itemListElement":['
          f'{{"@type":"ListItem","position":1,"name":"Home","item":"{BASE}/"}},'
          f'{{"@type":"ListItem","position":2,"name":"Blog","item":"{BASE}/blog/"}},'
          f'{{"@type":"ListItem","position":3,"name":{json.dumps(c["title"],ensure_ascii=False)}}}]}},'
          f'{{"@type":"Article","headline":{json.dumps(c["title"],ensure_ascii=False)},'
          f'"description":{json.dumps(c["dek"],ensure_ascii=False)},"inLanguage":"{lang}",'
          f'"author":{{"@type":"Organization","name":"Anima Volitiva"}},'
          f'"publisher":{{"@id":"{BASE}/#organization"}},"image":"{BASE}/assets/hero.jpg"}}]}}')
    nav = (f'<nav><div class="wrap"><a class="brand" href="{home}">Anima <span>Volitiva</span></a>'
           f'<div class="nav-links"><a href="{blog}" class="active">{"Блог" if lang=="uk" else "Blog"}</a>'
           f'<a class="nav-cta" href="{home}#cta">{"Отримати аудит" if lang=="uk" else "Get assessment"}</a>'
           f'<span class="lang"><a class="on" href="#">{"UA" if lang=="uk" else "EN"}</a><span class="sep">|</span>'
           f'<a href="{alt_en if lang=="uk" else alt_uk}">{"EN" if lang=="uk" else "УКР"}</a></span></div></div></nav>')
    footer = (f'<footer><div class="wrap"><a class="brand" href="{home}" style="color:#cbb9a6">Anima '
              f'<span style="color:var(--accent)">Volitiva</span></a><div class="fnav">'
              f'<a href="{home}">{"Головна" if lang=="uk" else "Home"}</a><a href="{blog}">{"Блог" if lang=="uk" else "Blog"}</a>'
              f'<a href="{home}#cta">{"Отримати аудит" if lang=="uk" else "Get assessment"}</a></div>'
              f'<div>© 2026 Anima Volitiva · Kyiv &amp; Kyiv Oblast</div></div></footer>')
    doc = f'''<!DOCTYPE html><html lang="{lang}"><head>
<meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{html.escape(c["title"])} | Anima Volitiva</title>
<meta name="description" content="{html.escape(c["dek"])}" />
<link rel="stylesheet" href="{css}" /><link rel="canonical" href="{canon}"/>
<link rel="alternate" hreflang="en" href="{alt_en}"/><link rel="alternate" hreflang="uk" href="{alt_uk}"/>
<link rel="alternate" hreflang="x-default" href="{alt_en}"/>
<meta property="og:type" content="article"/><meta property="og:title" content="{html.escape(c["title"])}"/>
<meta property="og:description" content="{html.escape(c["dek"])}"/><meta property="og:url" content="{canon}"/>
<meta property="og:image" content="{BASE}/assets/hero.jpg"/><meta name="twitter:card" content="summary_large_image"/>
<script type="application/ld+json">{ld}</script><script src="{ana}" defer></script></head><body>
{nav}
<header class="page-hero" style="--ph:url('{hero}')"><div class="wrap">
  <div class="crumb"><a href="{home}">{'Головна' if lang=='uk' else 'Home'}</a> · <a href="{blog}">{'Блог' if lang=='uk' else 'Blog'}</a></div>
  <h1>{html.escape(c["title"])}</h1><p class="sub">{html.escape(c["dek"])}</p>
</div></header>
<article class="block"><div class="wrap" style="max-width:800px">
{md_to_html(c["intro"])}{secs_html}
</div></article>
<section class="cta block" id="cta"><div class="wrap" style="text-align:center">
  <h2>{'Порахувати ваш flat-rate' if lang=='uk' else 'See your flat-rate in one audit'}</h2>
  <a class="btn btn-primary" href="{home}#cta">{'Отримати безкоштовний аудит' if lang=='uk' else 'Get your free assessment'}</a>
</div></section>
{footer}</body></html>'''
    outdir = ROOT / ("ua/blog" if lang == "uk" else "blog")
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / SLUG).write_text(doc, encoding="utf-8")
    return c["title"], canon

def build_index(lang):
    c = UA if lang == "uk" else EN
    title, url = c["title"], f"{BASE}/{'ua/' if lang=='uk' else ''}blog/{SLUG}"
    up = "../../" if lang=="uk" else "../"
    home = "../index.html"
    css = up+"style.css"; ana = up+"assets/analytics.js"
    canon = f"{BASE}/{'ua/' if lang=='uk' else ''}blog/"
    nav = (f'<nav><div class="wrap"><a class="brand" href="{home}">Anima <span>Volitiva</span></a>'
           f'<div class="nav-links"><a href="{home}#cta" class="nav-cta">{"Отримати аудит" if lang=="uk" else "Get assessment"}</a>'
           f'<span class="lang"><a class="on" href="#">{"UA" if lang=="uk" else "EN"}</a></span></div></div></nav>')
    card = (f'<a href="{SLUG}" style="display:block;border:1px solid var(--line);border-radius:12px;'
            f'padding:24px 28px;text-decoration:none;max-width:760px"><span style="color:var(--accent);'
            f'font-weight:700;font-size:20px">{html.escape(c["title"])}</span>'
            f'<p style="margin:8px 0 0;color:var(--ink-soft)">{html.escape(c["dek"])}</p></a>')
    doc = f'''<!DOCTYPE html><html lang="{lang}"><head>
<meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{'Блог' if lang=='uk' else 'Blog'} | Anima Volitiva</title>
<meta name="description" content="{'Інсайти про B2B-кавові операції у Києві та області.' if lang=='uk' else 'Insights on B2B coffee operations in Kyiv & Kyiv Oblast.'}" />
<link rel="stylesheet" href="{css}" /><link rel="canonical" href="{canon}"/><script src="{ana}" defer></script></head><body>
{nav}
<header class="page-hero" style="--ph:url('{up}assets/cafe.jpg')"><div class="wrap">
  <div class="crumb"><a href="{home}">{'Головна' if lang=='uk' else 'Home'}</a> · {'Блог' if lang=='uk' else 'Blog'}</div>
  <h1>{'Блог' if lang=='uk' else 'Insights'}</h1>
  <p class="sub">{'Про кавові операції B2B у Києві та області.' if lang=='uk' else 'On running B2B coffee operations in Kyiv & Kyiv Oblast.'}</p>
</div></header>
<section class="block"><div class="wrap">{card}</div></section>
</body></html>'''
    outdir = ROOT / ("ua/blog" if lang == "uk" else "blog")
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "index.html").write_text(doc, encoding="utf-8")

for lg in ("en", "uk"):
    t, u = build_post(lg); build_index(lg); print(f"{lg}: post + index -> {u}")
