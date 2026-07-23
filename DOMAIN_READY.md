# Domain-ready

This site currently serves from GitHub Pages at
`https://dancanadian.github.io/anima-coffee-site/`. Every canonical URL,
hreflang alternate, Open Graph tag, JSON-LD `@id`/`url`, sitemap entry, and
`robots.txt`/`llms.txt` reference is derived from that one base URL.

**This is documentation only.** No CNAME file is committed and no DNS/domain
change has been made — those are founder + Conductor gated (ADR-027: DNS is
managed via adm.tools, not touched from this repo or by cloud agents).

## To go live on `aeo.animacoffee.com.ua`

1. **DNS (adm.tools, founder/Conductor gate):** add a `CNAME` record for
   `aeo.animacoffee.com.ua` pointing at `dancanadian.github.io`.
2. **Repoint the site's own URLs — one command:**
   ```
   python3 tools/set_base_url.py https://aeo.animacoffee.com.ua
   ```
   This rewrites every canonical/hreflang/OG/JSON-LD/sitemap/robots/llms.txt
   reference across the repo in one pass (dry-run first with `--dry-run` to
   preview). Commit and push the result.
3. **GitHub Pages custom domain:** in the repo's Pages settings, set the
   custom domain to `aeo.animacoffee.com.ua`. GitHub will commit a `CNAME`
   file automatically at that point — this is expected and is the one time a
   CNAME file should exist in this repo.
4. **Verify:** re-run `python3 tools/aeo_seo_check.py` and
   `curl -I https://aeo.animacoffee.com.ua/` for a 200, then spot-check a
   handful of EN/UA/answer pages.

Nothing else in the codebase needs to change — the engine, content, and gates
are already domain-agnostic.
