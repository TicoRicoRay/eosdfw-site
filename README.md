# EOSDFW.com

Static marketing site for **Ray Myers, Professional EOS Implementer®** serving the Dallas–Fort Worth metroplex.

## Stack

- Plain HTML + CSS + tiny vanilla JS
- Jinja2 templates rendered at build time by `build.py`
- Deployed to GitHub Pages, fronted by Cloudflare
- Primary domain: `eosdfw.com` (canonical) — `dfweos.com` should 301-redirect via a Cloudflare Page Rule

## Local development

```bash
pip install jinja2
python3 build.py
# Serve locally:
python3 -m http.server 8000
# → http://localhost:8000
```

## File layout

```
templates/
  base.html              # shared head + JSON-LD schema
  partials/
    header.html          # sticky nav, theme toggle, mobile menu
    footer.html          # links + EOS trademark attribution
  pages/
    index.html, about.html, contact.html, 90-minute-meeting.html
    services/index.html, eos-process.html, focus-day.html,
             vision-building.html, quarterly-annual.html
    insights/index.html
css/style.css            # all visual styling, light + dark mode
js/main.js               # theme toggle + mobile menu (<1KB)
images/favicon.svg       # custom mark (not EOS logo)
build.py                 # render templates → HTML, generate sitemap + robots
```

Rendered HTML, `sitemap.xml`, and `robots.txt` are committed at the repo root so GitHub Pages serves them directly.

## EOS branding compliance

This site follows [EOS Worldwide branding guidelines](https://branding.eosworldwide.com/):

- Registered marks (®) and common-law marks (™) on **first use per page**
- Trademark attribution block in the footer
- No EOS logos, badges, or licensed brand assets
- No non-EOS services offered alongside EOS content
- *Traction* book title italicized; never trademarked
- Words like "vision", "data", "process" lowercase when used non-process-wise

See `COMPLIANCE.md` for the full review checklist.

## Adding a blog post

1. Drop a new file in `templates/pages/insights/` (e.g., `post-slug.html`)
2. Add an entry to `PAGES_MANIFEST` in `build.py`
3. Add a card on `templates/pages/insights/index.html`
4. `python3 build.py` → commit → push
