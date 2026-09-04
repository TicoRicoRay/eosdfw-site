#!/usr/bin/env python3
"""
EOSDFW.com static site builder.


Renders Jinja2 templates from `templates/` into the project root as plain HTML.
GitHub Pages serves the HTML files directly. Run `python3 build.py` to rebuild.
"""
import os
import sys
import shutil
from pathlib import Path

try:
    from jinja2 import Environment, FileSystemLoader, select_autoescape
except ImportError:
    print("Missing jinja2. Install with: pip install jinja2", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent
TEMPLATES = ROOT / "templates"
PAGES = TEMPLATES / "pages"
OUT = ROOT

SITE = {
    "site_name": "Ray Myers — EOS Implementer® in DFW",
    "site_url": "https://eosdfw.com",
    "primary_email": "ray.myers@eosworldwide.com",
    "calendly": "https://calendly.com/rmyers/eos-90",
    "phone": None,  # not published per the EOS profile
    "linkedin": "https://www.linkedin.com/in/raymyers",
    "youtube": "https://www.youtube.com/@RayMyersBusinessCoach",
}

# YouTube content — pulled from @RayMyersBusinessCoach.
# Featured video shows on the home page; the full grid renders on About.
FEATURED_VIDEO = {
    "id": "6LC4HxK2e0w",
    "title": "Discover EOS® — For Free",
    "duration": "2:47",
}
VIDEOS = [
    {"id": "6LC4HxK2e0w", "title": "Discover EOS® — For Free", "duration": "2:47"},
    {"id": "PvTo-eOMnww", "title": "Living Your Ideal Entrepreneurial Life", "duration": "3:09"},
    {"id": "Mfujrpxw1mo", "title": "Do You Know Someone Who Owns a Business?", "duration": "1:29"},
    {"id": "uh4xqXgQSkg", "title": "Avoid Costly Hiring Mistakes", "duration": ""},
    {"id": "3xX5igLrkCo", "title": "Matching a Visionary with the Right Integrator", "duration": ""},
]

# Each entry: src template (relative to pages/), output path (relative to OUT),
# and page-specific metadata. `nav_key` ties to the active state in nav.
PAGES_MANIFEST = [
    {"src": "index.html",
     "out": "index.html",
     "title": "EOS Implementer in DFW | Ray Myers, Professional EOS Implementer®",
     "description": "Ray Myers is a Professional EOS Implementer® serving Dallas–Fort Worth business owners and leadership teams. Schedule a free 90 Minute Meeting to learn how EOS® can help you get more of what you want from your business.",
     "nav_key": "home"},

    {"src": "about.html",
     "out": "about.html",
     "title": "About Ray Myers | DFW EOS Implementer®",
     "description": "Meet Ray Myers — Professional EOS Implementer® based in the Dallas–Fort Worth metroplex. 30+ years as an entrepreneur, now helping leadership teams strengthen the Six Key Components® of their business.",
     "nav_key": "about"},

    {"src": "services/index.html",
     "out": "services/index.html",
     "title": "EOS Services in DFW | Focus Day®, Vision Building® & More",
     "description": "Working with Ray Myers as your EOS Implementer® means a clear, proven path. Focus Day®, Vision Building® Day 1 and Day 2, and ongoing Quarterly and Annual sessions — delivered across DFW and virtually.",
     "nav_key": "services"},

    {"src": "services/eos-process.html",
     "out": "services/eos-process.html",
     "title": "The EOS Process® in DFW | Ray Myers, EOS Implementer®",
     "description": "The EOS Process® is the proven way EOS Implementers® deliver the right tool at the right time — on average, 10 full days over two years. Here's what the journey looks like.",
     "nav_key": "services"},

    {"src": "services/focus-day.html",
     "out": "services/focus-day.html",
     "title": "Focus Day® in DFW | EOS Implementer® Ray Myers",
     "description": "Focus Day® is the kickoff day of the EOS Process®. Your leadership team leaves with five practical tools to start strengthening the Six Key Components® of your business.",
     "nav_key": "services"},

    {"src": "services/vision-building.html",
     "out": "services/vision-building.html",
     "title": "Vision Building® Day 1 & Day 2 in DFW | Ray Myers",
     "description": "Vision Building® Day 1 and Day 2 are where your leadership team gets 100% on the same page with where the company is going and how it plans to get there.",
     "nav_key": "services"},

    {"src": "services/quarterly-annual.html",
     "out": "services/quarterly-annual.html",
     "title": "Quarterly & Annual Sessions in DFW | EOS Implementer®",
     "description": "Quarterly and Annual sessions keep your leadership team focused, accountable, and aligned. Ray Myers facilitates ongoing EOS® sessions for DFW leadership teams.",
     "nav_key": "services"},

    {"src": "90-minute-meeting.html",
     "out": "90-minute-meeting.html",
     "title": "Free 90 Minute Meeting | DFW EOS Implementer® Ray Myers",
     "description": "Schedule your free, no-obligation 90 Minute Meeting with DFW EOS Implementer® Ray Myers. See exactly how EOS® can help your leadership team get more of what you want from your business.",
     "nav_key": "90min"},

    {"src": "insights/index.html",
     "out": "insights/index.html",
     "title": "EOS® Insights for Dallas–Fort Worth Business Owners | Ray Myers, DFW EOS Implementer®",
     "description": "Practical guidance on the Entrepreneurial Operating System® — Vision, Traction®, Scorecards, Level 10 Meetings®, and the EOS Life® — for DFW business owners and leadership teams. From Professional EOS Implementer® Ray Myers.",
     "nav_key": "insights"},

    {"src": "insights/flying-blind-scorecard.html",
     "out": "insights/flying-blind-scorecard.html",
     "title": "Flying Blind With Your Business? — The EOS Scorecard | Ray Myers, DFW EOS Implementer®",
     "description": "Most operators are drowning in data and starving for information. Here's how 5–15 numbers a week — the EOS® Scorecard — replaces the entire dashboard of guesses. By Ray Myers, Professional EOS Implementer® in DFW.",
     "nav_key": "insights"},

    {"src": "insights/rocket-fuel-visionary-integrator.html",
     "out": "insights/rocket-fuel-visionary-integrator.html",
     "title": "Matching a Visionary With the Right Integrator — Rocket Fuel® | Ray Myers, DFW EOS Implementer®",
     "description": "Steve Jobs had Woz. Walt had Roy. When the Visionary and Integrator click, it's Rocket Fuel®. Here's how to tell which seat you're in and what makes the pairing work. By Ray Myers, Professional EOS Implementer® in DFW.",
     "nav_key": "insights"},

    {"src": "insights/level-10-meeting-90-minute-fix.html",
     "out": "insights/level-10-meeting-90-minute-fix.html",
     "title": "The Level 10 Meeting®: The 90-Minute Weekly Leadership Meeting That Actually Works | DFW EOS Implementer®",
     "description": "Weekly leadership meetings feel like a waste because they default to status updates. Here's the seven-part Level 10 Meeting® agenda — 90 minutes, same time, every week — that turns meetings into decisions. By Ray Myers, Professional EOS Implementer® in DFW.",
     "nav_key": "insights"},

    {"src": "insights/people-analyzer-right-people-right-seats.html",
     "out": "insights/people-analyzer-right-people-right-seats.html",
     "title": "The People Analyzer®: Right People, Right Seats | Ray Myers, DFW EOS Implementer®",
     "description": "How to know if you have the right people in the right seats. A step-by-step guide to the EOS® People Analyzer, GWC (Get it, Want it, Capacity), core values ratings, and the Three-Strike Rule. By Ray Myers, Professional EOS Implementer® in DFW.",
     "nav_key": "insights"},

    {"src": "insights/ai-needs-a-foundation.html",
     "out": "insights/ai-needs-a-foundation.html",
     "title": "AI needs a foundation: Vision, Core Values, Right People | Ray Myers, DFW EOS Implementer®",
     "description": "AI is a powerful toolset, but a powerful tool amplifies whatever you point it at. A 30-year software founder and Professional EOS Implementer® on why Vision, Core Values, and Right People in the Right Seats are the foundation businesses need before making the AI leap.",
     "nav_key": "insights"},

    {"src": "insights/rocks-vs-todos-quarterly-priorities.html",
     "out": "insights/rocks-vs-todos-quarterly-priorities.html",
     "title": "Rocks vs. To-Dos: Why Your Team Keeps Missing Quarterly Priorities | Ray Myers, DFW EOS Implementer®",
     "description": "Most missed Rocks aren't a discipline problem, they're a definition problem. The difference between a Rock and a to-do, why 3 to 7 is the magic number, and how to set Q4 priorities your leadership team will actually hit. By Ray Myers, Professional EOS Implementer® in DFW.",
     "nav_key": "insights",
     "noindex": True},  # remove noindex flag + template meta tag on publish day

    {"src": "insights/eos-life-time-for-passions.html",
     "out": "insights/eos-life-time-for-passions.html",
     "title": "Time for Other Passions — The EOS Life® | Ray Myers, DFW EOS Implementer®",
     "description": "Tornado chasing, stage gigs, stunt work, astronaut training, indoor skydiving, and zip lining — what The EOS Life® actually looks like when the system works. By Ray Myers, Professional EOS Implementer® in DFW.",
     "nav_key": "insights"},

    {"src": "contact.html",
     "out": "contact.html",
     "title": "Contact Ray Myers | DFW EOS Implementer®",
     "description": "Get in touch with Ray Myers, Professional EOS Implementer® in the Dallas–Fort Worth metroplex. Email or book your free 90 Minute Meeting.",
     "nav_key": "contact"},

    {"src": "privacy.html",
     "out": "privacy.html",
     "title": "Privacy Policy | Ray Myers, DFW EOS Implementer®",
     "description": "Privacy policy for eosdfw.com. No trackers, no data sale, no marketing cookies. Details on what is collected, how it's used, and your California (CCPA/CPRA) and other privacy rights.",
     "nav_key": "privacy"},
]


def build():
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES)),
        autoescape=select_autoescape(["html"]),
        trim_blocks=False,
        lstrip_blocks=False,
    )

    for page in PAGES_MANIFEST:
        tpl = env.get_template(f"pages/{page['src']}")
        # Compute relative path prefix for assets (e.g., '../' for nested pages)
        depth = page["out"].count("/")
        asset_prefix = "../" * depth
        rendered = tpl.render(
            site=SITE,
            page=page,
            asset_prefix=asset_prefix,
            featured_video=FEATURED_VIDEO,
            videos=VIDEOS,
        )
        out_path = OUT / page["out"]
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(rendered, encoding="utf-8")
        print(f"  wrote {page['out']}")

    # Generate sitemap + robots + 404 alongside
    build_sitemap()
    build_robots()
    print("Done.")


def build_sitemap():
    from datetime import datetime
    today = datetime.utcnow().strftime("%Y-%m-%d")
    urls = []
    for page in PAGES_MANIFEST:
        if page.get("noindex"):
            continue
        loc = SITE["site_url"].rstrip("/") + "/" + page["out"]
        # Pretty URL for index pages
        loc = loc.replace("/index.html", "/")
        if loc.endswith("/index.html"):
            loc = loc[:-10]
        priority = "1.0" if page["out"] == "index.html" else "0.8"
        urls.append(
            f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{today}</lastmod>\n    <priority>{priority}</priority>\n  </url>"
        )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )
    (OUT / "sitemap.xml").write_text(xml, encoding="utf-8")
    print("  wrote sitemap.xml")


def build_robots():
    txt = (
        "User-agent: *\n"
        "Allow: /\n\n"
        f"Sitemap: {SITE['site_url']}/sitemap.xml\n"
    )
    (OUT / "robots.txt").write_text(txt, encoding="utf-8")
    print("  wrote robots.txt")


if __name__ == "__main__":
    build()
