#!/usr/bin/env python3
"""BASE_URL swap — the ONE place to repoint canonical/hreflang/og/JSON-LD/
sitemap/robots/llms.txt URLs when this site moves to a custom domain.

This is a static site with no build step, so "one swappable constant" means
one script argument, not a template variable. Every absolute site URL in the
repo is derived from CURRENT_BASE_URL below; running this script with a new
base URL rewrites every occurrence across every file in one pass.

Usage:
  python3 tools/set_base_url.py https://aeo.animacoffee.com.ua
  python3 tools/set_base_url.py https://aeo.animacoffee.com.ua --dry-run

Does NOT touch DNS, CNAME, or any founder-gated infra — see DOMAIN_READY.md.
"""
import argparse, pathlib, sys

CURRENT_BASE_URL = "https://aeo.animacoffee.com.ua"

EXTENSIONS = {".html", ".xml", ".txt"}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("new_base_url", help="e.g. https://aeo.animacoffee.com.ua (no trailing slash)")
    ap.add_argument("--site", default=str(pathlib.Path(__file__).resolve().parent.parent))
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    new_url = a.new_base_url.rstrip("/")
    old_url = CURRENT_BASE_URL.rstrip("/")
    if new_url == old_url:
        print("New base URL matches CURRENT_BASE_URL — nothing to do.")
        return

    site = pathlib.Path(a.site)
    changed = 0
    for path in sorted(site.rglob("*")):
        if path.suffix not in EXTENSIONS or not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if old_url not in text:
            continue
        count = text.count(old_url)
        if a.dry_run:
            print(f"{path.relative_to(site)}: {count} occurrence(s) would change")
        else:
            path.write_text(text.replace(old_url, new_url), encoding="utf-8")
            print(f"{path.relative_to(site)}: {count} occurrence(s) updated")
        changed += 1

    if not a.dry_run:
        # keep this script's own default in sync for the next run
        script = pathlib.Path(__file__)
        src = script.read_text(encoding="utf-8")
        script.write_text(
            src.replace(f'CURRENT_BASE_URL = "{old_url}"', f'CURRENT_BASE_URL = "{new_url}"'),
            encoding="utf-8",
        )
        print(f"\nUpdated CURRENT_BASE_URL in {script.name} for future runs.")
    print(f"\n{'Would touch' if a.dry_run else 'Touched'} {changed} file(s).")
    print("Reminder: this does not add a CNAME file or touch DNS/Pages settings — see DOMAIN_READY.md.")

if __name__ == "__main__":
    sys.exit(main())
