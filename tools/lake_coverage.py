#!/usr/bin/env python3
"""Lake-consumption gate — anti-inert-registry for CONTENT.

Measures what fraction of the PAID deep-research lake actually reaches rendered
pages. Blocks "client-ready" until coverage >= threshold. This is the mechanism
that stops the recurring "site shipped from 15% of the lake" failure
(postmortem 2026-07-23): "done" must mean paid-substrate-consumed, not just
page-passes-a-gate.

Usage: python3 tools/lake_coverage.py [--lake DIR] [--min 0.85]
Exit 0 if every mapped core page renders >= --min of its source prose, else 1.
"""
import argparse, pathlib, re, sys

# rich Landing_Page.md  ->  built HTML page
CORE_MAP = {
    "home_Landing_Page.md": "index.html",
    "how_to_rent_a_professional_coffee_machine_in_kyiv_Landing_Page.md": "how-to-rent.html",
    "monthly_coffee_service_contract_what_s_included_Landing_Page.md": "monthly-contract.html",
    "coffee_machine_maintenance_and_24_7_support_in_kyiv_oblast_Landing_Page.md": "maintenance.html",
    "specialty_coffee_bean_supply_for_offices_and_horeca_Landing_Page.md": "specialty-beans.html",
    "barista_staff_training_for_office_coffee_setups_Landing_Page.md": "barista-training.html",
    "swiss_super_automatic_vs_commercial_espresso_machines_Landing_Page.md": "swiss-vs-commercial.html",
}
DEFAULT_LAKE = "/mnt/c/Dev Antigravity/ADV AI HUB/deep_research/output/Anima_Volitiva_0619_LAKEJOIN_REAL_KG"

def words(s): return len(re.findall(r"\w+", s))
def visible(html): return words(re.sub(r"<[^>]+>", " ", html))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lake", default=DEFAULT_LAKE)
    ap.add_argument("--site", default=str(pathlib.Path(__file__).resolve().parent.parent))
    ap.add_argument("--min", type=float, default=0.85)
    a = ap.parse_args()
    lake, site = pathlib.Path(a.lake), pathlib.Path(a.site)
    ok = True
    print(f"{'PAGE':26} {'src':>6} {'built':>6} {'%':>5} {'kg':>4}  verdict")
    for md, page in CORE_MAP.items():
        src = lake / md; pg = site / page
        if not src.exists(): print(f"{page:26} MISSING SOURCE {md}"); ok = False; continue
        if not pg.exists(): print(f"{page:26} MISSING PAGE"); ok = False; continue
        sp, bp = words(src.read_text(encoding="utf-8", errors="ignore")), visible(pg.read_text(encoding="utf-8", errors="ignore"))
        kg = len(re.findall(r"data-kg-(ref|triple)", pg.read_text(encoding="utf-8", errors="ignore")))
        ratio = bp / sp if sp else 0
        good = ratio >= a.min and kg > 0
        ok = ok and good
        print(f"{page:26} {sp:6} {bp:6} {ratio*100:4.0f}% {kg:4}  {'PASS' if good else 'FAIL'}")
    print(f"\nGATE: {'PASS — lake consumed >= %.0f%% on all core pages' % (a.min*100) if ok else 'FAIL — under-consumed lake or missing KG grounding'}")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
