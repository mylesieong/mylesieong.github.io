#!/usr/bin/env python3
"""Render the hub pages of mylesieong.github.io.

The parent site carries the brand, the product index and the SEO trees for the
products that do not have their own repository. Product sites that live in their
own repo are mounted as submodules under products/ and are NOT touched by this
script -- see README.md.

    python3 build.py

Every page below is generated. Anything not listed in PAGES is hand-maintained.
"""

import html
import os
import re
import shutil
from datetime import date

SITE = "https://mylesieong.github.io"
ROOT = os.path.dirname(os.path.abspath(__file__))
TODAY = date.today().isoformat()

BRAND = "Sai vs. Reality"
TAGLINE = "Building in public. Failing with documentation."
HANDLE = "@saivsreality"
AUTHOR = "Myles Ieong"

STATUS_LABEL = {
    "live": "Live",
    "beta": "Beta",
    "building": "Building",
    "killed": "Killed",
}

# --------------------------------------------------------------------------
# Products. To add one, append a dict here and run build.py.
# `path`  - URL path from the site root, no trailing index.html
# `owner` - "submodule" (its own repo, never edited by this script) or "hub"
# --------------------------------------------------------------------------

PRODUCTS = [
    dict(slug="runout-rank", name="Runout Rank", status="live", owner="submodule",
         path="/products/runout-rank/",
         icon="/assets/icons/runout-rank.png",
         line="A pool rating from ten generated table layouts instead of 200 league games."),
    dict(slug="pool-billiards-self-trainer", name="Pool &amp; Billiards Self-Trainer",
         status="live", owner="submodule",
         path="/products/pool-billiards-self-trainer/",
         icon="/assets/icons/pool-billiards-self-trainer.png",
         line="Drills, skill exams and match tracking for practising pool on your own."),
    dict(slug="snooker-self-trainer", name="Snooker Self-Trainer", status="live", owner="submodule",
         path="/products/snooker-self-trainer/",
         icon="/assets/icons/snooker-self-trainer.png",
         line="The same structure as the pool trainer, rebuilt for a twelve-foot table."),
    dict(slug="bible-project", name="Bible Project", status="live", owner="submodule",
         path="/products/bible-project/",
         icon="/assets/icons/bible-project.png",
         line="KJV and ESV offline, with an AI that answers when you have a question."),
    dict(slug="flexi", name="Flexi", status="live", owner="submodule",
         path="/products/flexi/",
         icon="/assets/icons/flexi.png",
         line="Timed, illustrated stretching plans with voice guidance. Built for a habit, not a workout."),
    dict(slug="tacet", name="Tacet", status="live", owner="submodule",
         path="/products/tacet/",
         icon="/assets/icons/tacet.png",
         line="Breathing paced by vibration with the screen off, so nobody in the room notices."),
    dict(slug="calmly-news", name="Calmly News", status="live", owner="hub",
         path="/products/calmly-news/",
         icon="/assets/icons/calmly-news.png",
         line="Ten stories a day, stripped of drama adjectives. Then the feed locks."),
    dict(slug="sai-studio", name="Sai Studio", status="live", owner="hub",
         path="/sai-studio/",
         icon=None,
         line="MVP builds for non-technical founders. The consulting arm that pays for the rest of this."),
    dict(slug="canieat", name="CanIEat", status="building", owner="submodule",
         path="/products/canieat/",
         icon=None,
         line="Does this one thing fit your diet, at your limit? Judgment pages while the scanner gets built."),
    dict(slug="chatengage", name="Chatengage", status="building", owner="hub",
         path="/chatengage/",
         icon=None,
         line="Send documents as one package with a bot that answers questions about them."),
    dict(slug="harness-survey", name="Harness Survey", status="live", owner="hub",
         path="/products/harness-survey/",
         icon=None,
         line="A survey that reads each answer and writes the follow-up question itself."),
    dict(slug="founders-note", name="Founder's Note", status="killed", owner="hub",
         path="/founders-note/",
         icon=None,
         line="A workspace built around one agent holding the whole company in memory. Killed during ideation."),
]

BY_SLUG = dict((p["slug"], p) for p in PRODUCTS)


def shipped(p):
    return p["status"] != "killed"


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def esc(s):
    """Escape for HTML. Unescapes first so entity-bearing source copy
    (&mdash;, &amp;) survives a round trip instead of becoming &amp;mdash;."""
    return html.escape(html.unescape(s), quote=True)


def status_pill(status):
    return ('<span class="status status-%s">%s</span>'
            % (status, STATUS_LABEL[status]))


def head(title, desc, path, og_image, extra_ld=None, noindex=False):
    """Build a complete, non-templated <head>."""
    url = SITE + path
    img = SITE + og_image
    bits = [
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        '<title>%s</title>' % esc(title),
        '<meta name="description" content="%s">' % esc(desc),
        '<link rel="canonical" href="%s">' % esc(url),
    ]
    if noindex:
        bits.append('<meta name="robots" content="noindex, follow">')
    bits += [
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="%s">' % esc(BRAND),
        '<meta property="og:title" content="%s">' % esc(title),
        '<meta property="og:description" content="%s">' % esc(desc),
        '<meta property="og:url" content="%s">' % esc(url),
        '<meta property="og:image" content="%s">' % esc(img),
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="twitter:title" content="%s">' % esc(title),
        '<meta name="twitter:description" content="%s">' % esc(desc),
        '<meta name="twitter:image" content="%s">' % esc(img),
        '<link rel="icon" href="/favicon.ico" sizes="any">',
        '<link rel="icon" type="image/png" href="/assets/icons/favicon-512.png" sizes="512x512">',
        '<link rel="apple-touch-icon" href="/assets/icons/apple-touch-icon.png">',
        '<link rel="stylesheet" href="/assets/css/site.css">',
    ]
    for ld in (extra_ld or []):
        bits.append('<script type="application/ld+json">\n%s\n</script>' % ld.strip())
    return "\n  ".join(bits)


def nav(current):
    items = [("/products/", "Products"), ("/killed/", "Killed")]
    if BUILD_LOG:
        items.append(("/build-log/", "Build log"))
    items.append(("/about/", "About"))
    out = []
    for href, label in items:
        cur = ' aria-current="page"' if href == current else ''
        out.append('<a href="%s"%s>%s</a>' % (href, cur, label))
    return "\n        ".join(out)


def header(current=""):
    return """<header class="site-header">
    <div class="wrap">
      <a class="brand" href="/">Sai <span class="brand-vs">vs.</span> Reality</a>
      <nav class="site-nav" aria-label="Main">
        %s
      </nav>
    </div>
  </header>""" % nav(current)


def footer():
    return """<footer class="site-footer">
    <div class="wrap">
      <ul class="footer-links">
        <li><a href="/products/">Products</a></li>
        <li><a href="/killed/">Killed products</a></li>%s
        <li><a href="/about/">About</a></li>
        <li><a href="/sai-studio/">Sai Studio</a></li>
        <li><a href="/field-notes/">Field notes</a></li>
      </ul>
      <p class="footer-motto">%s &mdash; %s</p>
      <p>%s &middot; <a href="https://github.com/mylesieong">github.com/mylesieong</a> &middot; <a href="mailto:myles.ieong@gmail.com">myles.ieong@gmail.com</a></p>
      <p class="footer-motto">Apps published by Municornio Ltd.</p>
    </div>
  </footer>""" % ('\n        <li><a href="/build-log/">Build log</a></li>' if BUILD_LOG else "",
                  esc(BRAND), esc(TAGLINE), esc(HANDLE))


def crumbs(trail):
    """trail: list of (path, label); last item is the current page."""
    lis = []
    for i, (path, label) in enumerate(trail):
        if i == len(trail) - 1:
            lis.append('<li><span aria-current="page">%s</span></li>' % esc(label))
        else:
            lis.append('<li><a href="%s">%s</a></li>' % (path, esc(label)))
    return """<nav class="crumbs wrap" aria-label="Breadcrumb">
    <ol>
      %s
    </ol>
  </nav>""" % ("\n      ".join(lis))


def breadcrumb_ld(trail):
    items = []
    for i, (path, label) in enumerate(trail):
        items.append(
            '      {"@type": "ListItem", "position": %d, "name": %s, "item": "%s"}'
            % (i + 1, _json_str(label), SITE + path))
    return ('{\n  "@context": "https://schema.org",\n  "@type": "BreadcrumbList",\n'
            '  "itemListElement": [\n%s\n  ]\n}' % (",\n".join(items)))


def _json_str(s):
    return '"%s"' % s.replace("\\", "\\\\").replace('"', '\\"').replace("&amp;", "&").replace("&nbsp;", " ")


def page(path, title, desc, og_image, body, trail=None, extra_ld=None,
         noindex=False, wide=False, current=""):
    lds = list(extra_ld or [])
    if trail:
        lds.append(breadcrumb_ld(trail))
    doc = """<!DOCTYPE html>
<html lang="en">
<head>
  %s
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  %s
  %s
  <main id="main" class="wrap%s">
%s
  </main>
  %s
</body>
</html>
""" % (head(title, desc, path, og_image, lds, noindex),
       header(current),
       crumbs(trail) if trail else "",
       " wrap-wide" if wide else "",
       body.rstrip(),
       footer())
    write(path, doc)


def write(path, doc):
    rel = path.lstrip("/")
    if rel == "" or rel.endswith("/"):
        rel += "index.html"
    dest = os.path.join(ROOT, rel)
    d = os.path.dirname(dest)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    with open(dest, "w") as f:
        f.write(doc)
    PAGES.append(path)


PAGES = []


# --------------------------------------------------------------------------
# images: real width/height on every <img> so nothing shifts (CLS)
# --------------------------------------------------------------------------

try:
    from PIL import Image
except ImportError:
    Image = None

_dim_cache = {}


def dims(src):
    """Real pixel size of a repo-relative image, for width/height attributes."""
    if src in _dim_cache:
        return _dim_cache[src]
    from urllib.parse import unquote
    p = os.path.join(ROOT, unquote(src).lstrip("/"))
    wh = (None, None)
    if p.lower().endswith(".svg") and os.path.exists(p):
        with open(p, errors="ignore") as f:
            head_txt = f.read(1024)
        m = re.search(r'viewBox="[\d.\-]+ +[\d.\-]+ +([\d.]+) +([\d.]+)"', head_txt)
        if not m:
            m = re.search(r'width="([\d.]+)[a-z"\s][^>]*height="([\d.]+)', head_txt)
        if m:
            wh = (int(round(float(m.group(1)))), int(round(float(m.group(2)))))
    elif Image and os.path.exists(p):
        try:
            with Image.open(p) as im:
                wh = im.size
        except Exception:
            pass
    _dim_cache[src] = wh
    return wh


def img(src, alt, cls=None, lazy=True):
    w, h = dims(src)
    a = ['src="%s"' % src, 'alt="%s"' % esc(alt)]
    if w:
        a.append('width="%d" height="%d"' % (w, h))
    if cls:
        a.append('class="%s"' % cls)
    if lazy:
        a.append('loading="lazy" decoding="async"')
    return "<img %s>" % " ".join(a)


def product_row(p):
    if p.get("icon"):
        w, h = dims(p["icon"])
        size = ' width="%d" height="%d"' % (w, h) if w else ""
        icon = ('<img src="%s" alt="" class="product-icon"%s loading="lazy" decoding="async">'
                % (p["icon"], size))
    else:
        initial = html.unescape(p["name"]).strip()[:1].upper()
        icon = '<span class="product-icon product-icon-letter" aria-hidden="true">%s</span>' % initial
    return """      <li>
        <a class="product-row" href="%s">
          %s
          <span class="product-body">
            <span class="product-name">%s</span>%s
            <span class="product-line">%s</span>
          </span>
        </a>
      </li>""" % (p["path"], icon, p["name"], status_pill(p["status"]), p["line"])


def product_list(products):
    return ('    <ul class="product-list">\n%s\n    </ul>'
            % "\n".join(product_row(p) for p in products))


# --------------------------------------------------------------------------
# homepage
# --------------------------------------------------------------------------

def build_home():
    live = [p for p in PRODUCTS if shipped(p)]
    dead = [p for p in PRODUCTS if not shipped(p)]

    website_ld = """{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "@id": "%(site)s/#website",
  "name": "%(brand)s",
  "alternateName": "%(handle)s",
  "url": "%(site)s/",
  "description": "%(tagline)s",
  "inLanguage": "en",
  "publisher": { "@id": "%(site)s/about/#person" }
}""" % dict(site=SITE, brand=BRAND, handle=HANDLE, tagline=TAGLINE)

    itemlist_ld = """{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "Products",
  "itemListOrder": "https://schema.org/ItemListUnordered",
  "numberOfItems": %d,
  "itemListElement": [
%s
  ]
}""" % (len(PRODUCTS), ",\n".join(
        '    {"@type": "ListItem", "position": %d, "name": %s, "url": "%s"}'
        % (i + 1, _json_str(p["name"]), SITE + p["path"])
        for i, p in enumerate(PRODUCTS)))

    body = """    <div class="hero">
      <h1>Sai vs. Reality</h1>
      <p class="tagline">Building in public. Failing with documentation.</p>
      <p class="lede lede-wide">I ship software into unrelated categories &mdash; pool practice, breathing, Bible reading, news &mdash; and Reality tells me which ones were wrong. Those stay published too, with the evidence.</p>
    </div>

    <h2 id="products">Products</h2>
    <p class="section-note">Every one of them, with what it actually is and where it actually stands.</p>
%s

    <h2 id="killed">Killed</h2>
    <p class="section-note">Products Reality closed. They keep their URL and gain a post-mortem: what I believed, what I built, what the evidence said, what I would do differently.</p>
%s
    <p><a href="/killed/">All post-mortems &rarr;</a></p>

%s
    <h2 id="about">Why any of this</h2>
    <p>Build less. Learn faster. Kill sooner. Try again.</p>
    <p>I'm not trying to become successful. I'm trying to become less stupid. Building a lot of small things across unrelated categories is the cheapest way I have found to be wrong quickly and in public. <a href="/about/">More about how this works &rarr;</a></p>
""" % (product_list(live), product_list(dead), build_log_teaser())

    page("/", "Sai vs. Reality &mdash; building in public, failing with documentation",
         "I ship small software products across unrelated categories and publish what happens, including the ones that failed. Pool training, breathing, Bible reading, news, and the post-mortems.",
         "/assets/og/home.png", body,
         extra_ld=[website_ld, itemlist_ld], current="")


def build_log_teaser():
    """Renders the homepage build-log section, or nothing at all when there are
    no posts. An empty section advertising a build log is worse than no
    section."""
    posts = BUILD_LOG
    if not posts:
        return ""
    latest = posts[0]
    return """    <h2 id="build-log">Build log</h2>
    <p class="section-note">What I am building, what broke, and what the numbers actually said.</p>
    <ul class="subpages">
      <li><a href="%s">%s<span class="sub-line">%s &middot; %s</span></a></li>
    </ul>
    <p><a href="/build-log/">All build-log posts &rarr;</a></p>""" % (
        latest["path"], esc(latest["title"]), latest["date"], esc(latest["blurb"]))


# --------------------------------------------------------------------------
# build log. To add a post: append a dict, newest first, and run build.py.
# --------------------------------------------------------------------------

BUILD_LOG = []


BUILD_LOG_BY_SLUG = dict((p["slug"], p) for p in BUILD_LOG)


def build_build_log():
    if not BUILD_LOG:
        return
    trail = [("/", "Home"), ("/build-log/", "Build log")]
    if BUILD_LOG:
        rows = "\n".join(
            '      <li><a href="%s">%s<span class="sub-line">%s &middot; %s</span></a></li>'
            % (p["path"], esc(p["title"]), p["date"], esc(p["blurb"])) for p in BUILD_LOG)
        body = """    <div class="hero">
      <h1>Build log</h1>
      <p class="lede">What I am building, what broke, and what the numbers actually said.</p>
    </div>
    <ul class="subpages">
%s
    </ul>
""" % rows
    else:
        body = """    <div class="hero">
      <h1>Build log</h1>
      <p class="lede">What I am building, what broke, and what the numbers actually said.</p>
    </div>
    <p>Nothing published yet.</p>
"""
    page("/build-log/", "Build log &mdash; Sai vs. Reality",
         "What I am building, what broke, and what the numbers actually said. Notes from shipping small software products across unrelated categories.",
         "/assets/og/build-log.png", body, trail=trail,
         noindex=not BUILD_LOG, current="/build-log/")

    for p in BUILD_LOG:
        t = trail + [(p["path"], p["title"])]
        article_ld = """{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": %s,
  "description": %s,
  "datePublished": "%s",
  "dateModified": "%s",
  "image": "%s",
  "mainEntityOfPage": { "@type": "WebPage", "@id": "%s" },
  "author": { "@id": "%s/about/#person" },
  "publisher": { "@id": "%s/#website" },
  "inLanguage": "en"
}""" % (_json_str(p["title"]), _json_str(p["desc"]), p["date"], p["date"],
        SITE + p["og"], SITE + p["path"], SITE, SITE)
        body = """    <div class="hero">
      <h1>%s</h1>
      <p class="lede lede-wide">%s</p>
      <p class="section-note"><time datetime="%s">%s</time></p>
    </div>
%s
    <hr>
    <p><a href="/build-log/">&larr; All build-log posts</a></p>
""" % (esc(p["title"]), esc(p["blurb"]), p["date"], p["date"], p["body"])
        page(p["path"], p["title"] + " &mdash; Sai vs. Reality", p["desc"], p["og"],
             body, trail=t, extra_ld=[article_ld], current="/build-log/")


# --------------------------------------------------------------------------
# post-mortems for killed products (section 4 of the brief)
#
# TODO(myles): fill in `believed`, `evidence` and `differently` for
# founders-note. They are the four questions the section exists to answer and
# I will not invent them. Anything left as None renders as "Not yet written."
# --------------------------------------------------------------------------

POSTMORTEMS = {
    "founders-note": dict(
        killed_on="late June 2026",
        believed="That founders were paying a real price for context switching. I was in "
                 "an incubator at the time, watching people hold a dozen streams of "
                 "information at once, and I assumed that if all of it lived in one place "
                 "with a single agent on top, they would pay to stop paying that price.",
        built="Nothing. The pitch, the positioning and this page, and that is the whole "
              "list. It was killed during ideation, before a line of the product was "
              "written.",
        evidence="Talking to founders through the ideation phase. The context-switching "
                 "cost was real and they recognised it immediately \u2014 and none of them "
                 "wanted to pay for it. The problem was not painful enough to be worth "
                 "money. They were handling it badly and were entirely willing to keep "
                 "handling it badly.",
        differently="Nothing about the kill itself. I had only spent time on the landing "
                    "page, so stopping cost me almost nothing, and I would stop again. What "
                    "I would change is the evidence I stopped on. I judged it from a handful "
                    "of conversations with the two or three founders I could actually reach, "
                    "and that is a sample small enough that \u201cnobody wants this\u201d and "
                    "\u201cI asked the wrong three people\u201d look exactly the same from "
                    "the inside. I should have put it in front of a much larger group first "
                    "\u2014 posted it publicly, on social, let a few hundred people ignore it "
                    "or not \u2014 before concluding on my own that it would not work."
    ),
}


def pm_dl(slug):
    pm = POSTMORTEMS.get(slug)
    if not pm:
        return ""
    rows = [("What I believed", pm["believed"]),
            ("What I built", pm["built"]),
            ("What the evidence said", pm["evidence"]),
            ("What I would do differently", pm["differently"])]
    out = []
    for label, val in rows:
        v = esc(val) if val else '<em class="section-note">Not yet written.</em>'
        out.append("      <dt>%s</dt>\n      <dd>%s</dd>" % (label, v))
    return '    <dl class="postmortem">\n%s\n    </dl>' % "\n".join(out)


def killed_banner(p):
    pm = POSTMORTEMS.get(p["slug"]) or {}
    when = (" in %s" % pm["killed_on"]) if pm.get("killed_on") else ""
    return """  <div class="wrap">
    <div class="killed-banner">
      <p><strong>%s is killed, and was never built.</strong> It was stopped during ideation%s. This page stays up and keeps its URL &mdash; nothing here is being redirected or deleted.</p>
      <p>Everything below this banner is the pitch as it stood, including the beta that never opened. <a href="#post-mortem">The post-mortem</a> is at the bottom of the page.</p>
    </div>
  </div>""" % (p["name"], when)


# --------------------------------------------------------------------------
# retrofitting the hand-built landing pages (sai-studio, chatengage,
# founders-note, field-notes). Their design is deliberate and stays; this only
# adds the head tags, the brand strip and any status banner, between markers,
# so re-running the build never duplicates anything.
# --------------------------------------------------------------------------

HEAD_START = "<!-- svr:head:start -->"
HEAD_END = "<!-- svr:head:end -->"
BODY_START = "<!-- svr:body:start -->"
BODY_END = "<!-- svr:body:end -->"
TAIL_START = "<!-- svr:tail:start -->"
TAIL_END = "<!-- svr:tail:end -->"


def _splice(text, start, end, payload, anchor, before=True):
    """Idempotently insert `payload` between markers, creating them if absent."""
    block = "%s\n%s\n%s" % (start, payload, end)
    pat = re.compile(re.escape(start) + ".*?" + re.escape(end), re.S)
    if pat.search(text):
        return pat.sub(lambda m: block, text, count=1)
    m = re.search(anchor, text, re.I)
    if not m:
        raise SystemExit("anchor %r not found" % anchor)
    at = m.start() if before else m.end()
    return text[:at] + block + "\n" + text[at:]


def retrofit(rel, title, desc, og_image, trail, extra_ld=None, banner="",
             tail="", noindex=False, keep_title=False):
    path = "/" + rel.rsplit("index.html", 1)[0]
    src = os.path.join(ROOT, rel)
    with open(src) as f:
        t = f.read()

    # the page's own <title>/<description> are replaced, not duplicated
    if not keep_title:
        t = re.sub(r"<title>.*?</title>", "<title>%s</title>" % esc(title), t, count=1, flags=re.S)
    t = re.sub(r'<meta\s+name="description"[^>]*>', "", t, count=1, flags=re.S | re.I)

    lds = list(extra_ld or [])
    if trail:
        lds.append(breadcrumb_ld(trail))
    headbits = [
        '<meta name="description" content="%s">' % esc(desc),
        '<link rel="canonical" href="%s">' % (SITE + path),
    ]
    if noindex:
        headbits.append('<meta name="robots" content="noindex, follow">')
    headbits += [
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="%s">' % esc(BRAND),
        '<meta property="og:title" content="%s">' % esc(title),
        '<meta property="og:description" content="%s">' % esc(desc),
        '<meta property="og:url" content="%s">' % (SITE + path),
        '<meta property="og:image" content="%s">' % (SITE + og_image),
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="twitter:title" content="%s">' % esc(title),
        '<meta name="twitter:description" content="%s">' % esc(desc),
        '<meta name="twitter:image" content="%s">' % (SITE + og_image),
        '<link rel="icon" href="/favicon.ico" sizes="any">',
        '<link rel="icon" type="image/png" href="/assets/icons/favicon-512.png" sizes="512x512">',
        '<link rel="apple-touch-icon" href="/assets/icons/apple-touch-icon.png">',
        '<link rel="stylesheet" href="/assets/css/site.css">',
    ]
    for ld in lds:
        headbits.append('<script type="application/ld+json">\n%s\n</script>' % ld.strip())
    t = _splice(t, HEAD_START, HEAD_END, "\n".join(headbits), r"</head>", before=True)

    strip = header() + ("\n" + crumbs(trail) if trail else "") + ("\n" + banner if banner else "")
    t = _splice(t, BODY_START, BODY_END, strip, r"<body[^>]*>", before=False)

    if tail:
        t = _splice(t, TAIL_START, TAIL_END, tail, r"<footer", before=True)

    with open(src, "w") as f:
        f.write(t)
    PAGES.append(path)


# --------------------------------------------------------------------------
# product index, killed index, about
# --------------------------------------------------------------------------

def build_products_index():
    trail = [("/", "Home"), ("/products/", "Products")]
    groups = [("live", "Live"), ("beta", "Beta"), ("building", "Building"), ("killed", "Killed")]
    parts = []
    for status, label in groups:
        items = [p for p in PRODUCTS if p["status"] == status]
        if not items:
            continue
        parts.append("    <h2 id=\"%s\">%s</h2>\n%s" % (status, label, product_list(items)))
    body = """    <div class="hero">
      <h1>Products</h1>
      <p class="lede lede-wide">Unrelated categories on purpose. If one of them dies it takes its own audience down with it and not the others.</p>
    </div>
%s
""" % "\n\n".join(parts)
    page("/products/", "Products &mdash; Sai vs. Reality",
         "Every product I have shipped or killed, with its current status: pool and snooker training, a pool rating test, a Bible reader, stretching, breathing, news, and consulting.",
         "/assets/og/products.png", body, trail=trail, current="/products/")


def build_killed_index():
    trail = [("/", "Home"), ("/killed/", "Killed")]
    dead = [p for p in PRODUCTS if not shipped(p)]
    rows = []
    for p in dead:
        rows.append('      <li><a href="%s">%s<span class="sub-line">%s</span></a></li>'
                    % (p["path"], p["name"], p["line"]))
    body = """    <div class="hero">
      <h1>Killed</h1>
      <p class="lede lede-wide">Products Reality closed. Each keeps its original URL and gains a post-mortem instead of a redirect, because the useful part of a dead product is the evidence that killed it.</p>
    </div>

    <p>Build less. Learn faster. Kill sooner. Try again. The third one is the part I am worst at, so it gets its own page.</p>

    <ul class="subpages">
%s
    </ul>

    <p class="section-note">Nothing on this list has been deleted or redirected, and nothing on it will be.</p>
""" % "\n".join(rows)
    page("/killed/", "Killed products and their post-mortems &mdash; Sai vs. Reality",
         "Products I shut down, each kept at its original URL with a post-mortem: what I believed, what I built, what the evidence said, and what I would do differently.",
         "/assets/og/killed.png", body, trail=trail, current="/killed/")


def build_about():
    trail = [("/", "Home"), ("/about/", "About")]
    person_ld = """{
  "@context": "https://schema.org",
  "@type": "Person",
  "@id": "%(site)s/about/#person",
  "name": "%(author)s",
  "alternateName": "%(handle)s",
  "url": "%(site)s/about/",
  "image": "%(site)s/assets/images/sai-headshot-192.png",
  "jobTitle": "Software developer",
  "description": "Builds and publishes small software products across unrelated categories, including the ones that failed.",
  "email": "mailto:myles.ieong@gmail.com",
  "sameAs": ["https://github.com/mylesieong"],
  "knowsAbout": ["Mobile app development", "iOS", "Android", "Product development"]
}""" % dict(site=SITE, author=AUTHOR, handle=HANDLE)

    body = """    <div class="hero">
      <h1>About</h1>
      <p class="lede lede-wide">I'm not trying to become successful. I'm trying to become less stupid.</p>
    </div>

    %s

    <p>My name is Myles Ieong. Everything I ship goes out under <strong>Sai vs. Reality</strong>, and everything under that name follows the same shape: I have an idea, I build it, Reality tells me I was wrong, I say &ldquo;interesting,&rdquo; and I keep going.</p>

    <h2>Why the products have nothing to do with each other</h2>
    <p>There is a pool training app, a snooker one, a pool rating test, a Bible reader, a stretching app, a breathing app and a news app on this site. That is not a strategy in the usual sense. It is the consequence of one: build small enough that being wrong costs weeks instead of years, and in enough different places that no single category has to be the one that works.</p>
    <p>The tradeoff is that no product inherits an audience. That is what this domain is for. One name people can decide to trust, carrying a set of products that individually could not have earned that on their own.</p>

    <h2>Build less. Learn faster. Kill sooner. Try again.</h2>
    <p>Build less, because most of what I build is a guess and a big guess is not more likely to be right than a small one. Learn faster, because the only thing a launch reliably produces is information. Kill sooner, because I am slow at it &mdash; <a href="/killed/">the killed products page</a> exists to make that failure visible to me as much as to anyone else. Try again, because that is the only step that compounds.</p>

    <h2>The numbers</h2>
    <p>When I publish numbers here they are evidence about a decision I made, not a scoreboard. If a product earned very little, the useful sentence is what I should have expected before I built it, not the figure on its own.</p>

    <h2>Contact</h2>
    <ul>
      <li>Email: <a href="mailto:myles.ieong@gmail.com">myles.ieong@gmail.com</a></li>
      <li>GitHub: <a href="https://github.com/mylesieong">github.com/mylesieong</a></li>
      <li>Consulting: <a href="/sai-studio/">Sai Studio</a></li>
      <li>Publishing partner: <a href="/partners/unicornio-macau/">Unicornio Macau Ltd</a></li>
    </ul>
""" % img("/assets/images/sai-headshot-192.png", "Myles Ieong", cls="product-icon")

    page("/about/", "About &mdash; Myles Ieong, Sai vs. Reality",
         "I build small software products across unrelated categories and publish what happens to them, including the failures. Why the products are unrelated, and what I do with the evidence.",
         "/assets/og/about.png", body, trail=trail, extra_ld=[person_ld], current="/about/")


def build_harness_survey():
    p = BY_SLUG["harness-survey"]
    trail = [("/", "Home"), ("/products/", "Products"), (p["path"], "Harness Survey")]

    app_ld = """{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "@id": "%(site)s/products/harness-survey/#app",
  "name": "Harness Survey",
  "url": "%(site)s/products/harness-survey/",
  "applicationCategory": "BusinessApplication",
  "applicationSubCategory": "Survey and research tool",
  "operatingSystem": "Web browser",
  "description": "A survey tool that reads each answer, writes the follow-up question itself, and routes every respondent into a segment at the end.",
  "installUrl": "https://harness-survey.vercel.app/",
  "author": { "@id": "%(site)s/about/#person" },
  "inLanguage": "en"
}""" % dict(site=SITE)

    body = """    <div class="hero">
      <h1>Harness Survey %s</h1>
      <p class="lede lede-wide">Your survey talks back. It reads each answer and writes the follow-up question itself.</p>
    </div>

    <div class="answer">
      <p>An ordinary survey asks &ldquo;how would you rate our pricing?&rdquo;, someone picks a 2, and that is all you ever get. Harness Survey reads the 2, notices what the person actually said, and asks the next question &mdash; the one you did not think to write.</p>
    </div>

    <ul class="stores">
      <li><a class="btn" href="https://harness-survey.vercel.app/">Open Harness Survey</a></li>
    </ul>

    <h2>What it does</h2>
    <ul>
      <li><strong>Follow-up questions written mid-conversation.</strong> Generated from what each person just answered, not picked from a branch you drew in advance. You choose the angle &mdash; clarification, hypothetical, follow-up &mdash; and it writes the wording.</li>
      <li><strong>Everyone leaves in a segment.</strong> Nobody ends on &ldquo;thanks for your response.&rdquo; Each respondent finishes in a group you defined, holding the offer meant for that group.</li>
      <li><strong>Results read back as themes.</strong> Grouped by what people meant, with the quotes underneath, rather than as rows to sort through yourself.</li>
    </ul>

    <div class="callout">
      <p><strong>The site you are reading is not its site yet.</strong> Harness Survey runs at <a href="https://harness-survey.vercel.app/">harness-survey.vercel.app</a>. It will get its own repository and be mounted here as a submodule, the way every other product on this domain is; until that happens this page is the placeholder holding the URL.</p>
    </div>

    <p><a href="/products/">&larr; All products</a></p>
""" % status_pill(p["status"])

    page(p["path"], "Harness Survey &mdash; the survey that writes its own follow-up",
         "A survey that reads every answer, writes the follow-up question itself, and sends each respondent out in a segment you defined.",
         "/assets/og/harness-survey.png", body, trail=trail,
         extra_ld=[app_ld], current="/products/")


# --------------------------------------------------------------------------
# Calmly News: the product page. It is the only product whose page lives in
# this repo rather than in its own; the rest are submodules and are not touched.
# No SEO pages anywhere -- the existing product sites keep the ones they have.
# --------------------------------------------------------------------------

CN = BY_SLUG["calmly-news"]
CN_APPSTORE = "https://apps.apple.com/us/app/calmly-news/id6756495260"
CN_PLAY = "https://play.google.com/store/apps/details?id=com.municornio.app.specialnewsapp"

CN_SHOTS = [
    ("/assets/images/calmly_news_1.jpg", "The daily feed, capped at ten stories"),
    ("/assets/images/calmly_news_2.jpg", "A story with the emotional language stripped out"),
    ("/assets/images/calmly_news_3.jpg", "Topic and keyword filters"),
    ("/assets/images/calmly_news_4.jpg", "The reset tools after a heavy story"),
]


def faq_ld(pairs):
    qs = []
    for q, a in pairs:
        plain = re.sub(r"<[^>]+>", "", a)
        qs.append("""    {
      "@type": "Question",
      "name": %s,
      "acceptedAnswer": { "@type": "Answer", "text": %s }
    }""" % (_json_str(q), _json_str(plain)))
    return ('{\n  "@context": "https://schema.org",\n  "@type": "FAQPage",\n'
            '  "mainEntity": [\n%s\n  ]\n}' % (",\n".join(qs)))


def faq_html(pairs):
    out = []
    for q, a in pairs:
        out.append("      <dt>%s</dt>\n      <dd>%s</dd>" % (esc(q), a))
    return '    <dl class="faq">\n%s\n    </dl>' % "\n".join(out)



def cn_stores():
    return """    <ul class="stores">
      <li><a class="btn" href="%s">Download on the App Store</a></li>
      <li><a class="btn btn-secondary" href="%s">Get it on Google Play</a></li>
    </ul>""" % (CN_APPSTORE, CN_PLAY)


def build_calmly_news():
    trail = [("/", "Home"), ("/products/", "Products"), (CN["path"], "Calmly News")]

    app_ld = """{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "@id": "%(site)s/products/calmly-news/#app",
  "name": "Calmly News",
  "url": "%(site)s/products/calmly-news/",
  "applicationCategory": "NewsApplication",
  "applicationSubCategory": "News reader",
  "operatingSystem": "iOS 15.0 or later, Android 8.0 or later",
  "description": "A news app with a ten-story daily cap, emotional language stripped from summaries, keyword filters and a reset step after heavy stories.",
  "inLanguage": "en",
  "image": "%(site)s/assets/images/calmly_news_logo.png",
  "screenshot": [%(shots)s],
  "installUrl": "%(appstore)s",
  "downloadUrl": "%(play)s",
  "author": { "@id": "%(site)s/about/#person" },
  "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD" }
}""" % dict(site=SITE, appstore=CN_APPSTORE, play=CN_PLAY,
            shots=", ".join('"%s%s"' % (SITE, s) for s, _ in CN_SHOTS))

    faqs = [
        ("What happens when I finish the ten stories?",
         "The feed locks for the rest of the day. There is no &ldquo;load more.&rdquo; That is the entire mechanism &mdash; the app is finished with you before you are finished with it."),
        ("Does it hide bad news?",
         "No. It removes the adjectives written to make a story land harder, not the story. A plane crash still reads as a plane crash. You can also filter specific topics or keywords, which does hide those, but that is a choice you make rather than something the app does on your behalf."),
        ("Is it free?",
         "Yes, on both iOS and Android."),
        ("Is this a mental health app?",
         "No, and it should not be used as one. It is a news reader with a cap and a filter. If news is affecting you in a way that a shorter feed does not fix, that is a conversation for a professional, not an app."),
    ]

    shots = "\n".join(
        '      <figure>%s<figcaption>%s</figcaption></figure>' % (img(s, cap), esc(cap))
        for s, cap in CN_SHOTS)

    body = """    <div class="hero">
      <h1>Calmly News %s</h1>
      <p class="lede lede-wide">Ten stories a day, with the drama adjectives stripped out. Then the feed locks.</p>
    </div>

    <div class="answer">
      <p>Every other news app is built to be bottomless, because time-in-app is the metric it is optimised against. Calmly News is built to end. Ten stories, chosen for the day, written without the language engineered to make you angry or afraid &mdash; and then nothing, until tomorrow.</p>
    </div>

%s

    <h2>What it actually does</h2>
    <ul>
      <li><strong>A hard cap of ten.</strong> Not a suggestion, a recommended-reading section, or a wellbeing nudge. When you have read the ten, the feed stops serving.</li>
      <li><strong>Summaries with the emotional loading removed.</strong> The adjectives that exist to make a headline hit harder are stripped; the facts of the story are not.</li>
      <li><strong>Filters you set.</strong> Block a topic or a keyword you do not have the capacity for this week. It stays blocked until you unblock it.</li>
      <li><strong>A reset after heavy stories.</strong> Some news is simply heavy. There are short breathing exercises built in for immediately afterwards, rather than a link to a different app.</li>
    </ul>

    <div class="shots">
%s
    </div>

    <h2>What it is not</h2>
    <p>It is not a way to avoid knowing things, and it is not a mental health tool. Mental health is not about hiding from the truth; it is about having the capacity to handle it. A ten-story cap protects your capacity. It does not do anything else, and I would rather say that here than imply otherwise.</p>

    <h2>Questions</h2>
%s
""" % (status_pill(CN["status"]), cn_stores(), shots, faq_html(faqs))

    page(CN["path"], "Calmly News &mdash; ten stories a day, then the feed locks",
         "A free news app with a hard ten-story daily cap, emotional language stripped from summaries, and keyword filters you control. iOS and Android.",
         "/assets/og/calmly-news.png", body, trail=trail,
         extra_ld=[app_ld, faq_ld(faqs)], current="/products/")


def build_cn_branches(parent_trail):
    up = ('    <p class="section-note"><a href="/products/calmly-news/">'
          '&larr; Calmly News</a></p>')

    # ---- best-<category>-app-for-<use-case> ----------------------------
    faqs_a = [
        ("Does a news app make anxiety worse or better?",
         "Either, depending on whether it ends. The mechanism that drives news anxiety is not information, it is the absence of a stopping point &mdash; there is always one more story, so there is never a moment where you have done enough. An app with a finite daily set gives you that moment. An infinite one cannot."),
        ("Should I just stop reading the news?",
         "Most people who try this do not last, and the ones who do often trade anxiety for a different discomfort about being uninformed. A daily cap is a smaller change with a much higher chance of surviving contact with a bad week."),
        ("Is there a news app that removes upsetting stories?",
         "Some let you filter topics, which is worth setting up honestly for the two or three subjects you genuinely cannot carry right now. Be wary of anything that filters by sentiment across the board &mdash; that is not a calmer news app, it is an inaccurate one."),
    ]
    body_a = """    <div class="hero">
      <h1>The best news app for anxiety is the one that ends</h1>
      <p class="lede lede-wide">A five-minute test you can run on any news app, including this one.</p>
    </div>

    <div class="answer">
      <p>Almost every &ldquo;calm news&rdquo; recommendation is about tone. Tone is the smaller half. The thing that actually drives news anxiety is that the feed has no end, so there is never a point at which you have finished and can put the phone down. Judge a news app on whether it stops.</p>
    </div>

    <h2>Three things that decide it</h2>
    <h3>1. Does the feed have a bottom?</h3>
    <p>Open the app and scroll. If you reach an end, note how long it took. If you do not reach an end, you have your answer: the app has delegated the stopping decision to you, at the exact moment you are least equipped to make it. Infinite scroll is not a neutral design choice, it is the product deciding that your session should be as long as you can bear.</p>

    <h3>2. Is the language doing work the facts are not?</h3>
    <p>Read five headlines and cross out every adjective and adverb. If the remaining sentence carries the same information, the app is reporting. If it collapses into something much smaller, the adjectives were the product. &ldquo;Officials slam shocking new figures&rdquo; contains one fact and two pieces of theatre.</p>

    <h3>3. Can you turn off a subject without turning off the app?</h3>
    <p>There are usually two or three subjects a person cannot carry in a given month. An app that lets you filter those by keyword lets you keep reading everything else. An app with no filtering leaves you with one lever: uninstall.</p>

    <h2>What to do if you are not changing apps</h2>
    <p>The cap matters more than the app. Decide the number of stories before you open anything, count them, and stop at the number even when the next headline is interesting &mdash; especially then. Read once a day rather than in fragments; the fragments are what keep the subject live in your head for sixteen hours. And read on a device you can put in another room.</p>
    <p>None of that requires software. The reason to use an app that enforces it is that a rule you have to apply yourself, several times a day, while a professionally optimised feed argues with you, is a rule you will lose.</p>

    <h2>Where Calmly News lands on its own test</h2>
    <p>It ends at ten stories, which is the whole reason it exists. It strips the emotional loading from summaries but not the stories themselves. It filters by topic and keyword. That is the entire pitch, and the three tests above are the ones I would want someone to run on it before believing me.</p>
    <p>What it does not do: it is not a treatment for anxiety, it has no idea how you are, and it will not soften a genuinely bad piece of news. If a shorter feed does not fix how the news is landing, the answer is not a different app.</p>

%s

    <h2>Questions</h2>
%s

%s
""" % (cn_stores(), faq_html(faqs_a), up)
    t = parent_trail + [(CN_SUBPAGES[0][0], "Best news app for anxiety")]
    page(CN_SUBPAGES[0][0],
         "Best news app for anxiety &mdash; judge it on whether the feed ends",
         "The thing that drives news anxiety is an infinite feed, not tone. Three tests to run on any news app in five minutes, and where Calmly News lands on them.",
         "/assets/og/cn-anxiety.png", body_a, trail=t,
         extra_ld=[faq_ld(faqs_a)], current="/products/")

    # ---- how-to-<job> --------------------------------------------------
    faqs_b = [
        ("Why is doomscrolling so hard to stop mid-scroll?",
         "Because the decision to stop has to be made repeatedly, against a feed that reloads faster than you can decide, at a time of day when your judgement is at its worst. It is not a willpower problem in any useful sense &mdash; you are being asked to win the same argument several hundred times."),
        ("Do screen-time limits work?",
         "Poorly, on their own. A timer interrupts you at an arbitrary point rather than a finished one, so it produces the feeling of being cut off rather than done, and the standard response is to tap &ldquo;ignore limit.&rdquo; A finite amount of content works better than a finite amount of time because it can actually be completed."),
        ("Is deleting the app the answer?",
         "It is the most effective single move and the least durable one. Most people reinstall within a fortnight, usually during exactly the news event that made them delete it. Worth doing as a reset, not as the plan."),
    ]
    body_b = """    <div class="hero">
      <h1>How to stop doomscrolling</h1>
      <p class="lede lede-wide">Four things that work, and one that everybody tries first.</p>
    </div>

    <div class="answer">
      <p>Doomscrolling is not a failure of self-control, it is the predictable result of pairing an infinite feed with a stopping rule that only you enforce. Fix the arrangement rather than your character: give the reading a defined end, a fixed time, and a physical distance.</p>
    </div>

    <h2>The one everybody tries first</h2>
    <p>Resolving to scroll less. This fails for a structural reason: the resolution has to be re-applied every few seconds, against a feed designed by people whose job is to make the next item feel worth one more swipe. You are not going to out-discipline a system that gets several hundred attempts per session.</p>

    <h2>1. Read a set, not a stream</h2>
    <p>Decide the number before you open anything &mdash; ten is a defensible figure for keeping up with the world &mdash; then read that many and stop. The point is not the number, it is that a set can be completed and a stream cannot. Completion is what produces the feeling of having done enough, and that feeling is the only reliable brake there is.</p>

    <h2>2. Once a day, not in fragments</h2>
    <p>Four two-minute checks are worse than one eight-minute read, even though the total is the same. Each check re-opens the subject and leaves it running in the background until the next one, so a fragmented habit keeps the news live in your head all day. One session has an end you can feel.</p>

    <h2>3. Not in bed</h2>
    <p>The scroll that does the damage is almost always the last one of the day, when your judgement about whether to stop is at its weakest and there is nothing scheduled afterwards to interrupt you. Charge the phone in another room. This is the single change with the best ratio of effect to effort, and it requires no software at all.</p>

    <h2>4. Cut the notifications, keep the news</h2>
    <p>Breaking-news alerts are the mechanism that converts a daily habit into an all-day one. Turning every news notification off does not make you less informed on any timescale that matters &mdash; you will find out about it in your session. It only removes the interruptions that start unplanned scrolls.</p>

    <h2>Where an app helps and where it does not</h2>
    <p>An app can enforce the first rule for you, which is the hard one. A feed that genuinely stops after a set number of stories removes the repeated decision entirely instead of asking you to keep making it. That is what Calmly News does: ten stories, then the feed locks for the day.</p>
    <p>It cannot do the other three. Reading once a day, staying out of bed with the phone, and killing notifications are habits, and no app installs a habit for you. Anything claiming otherwise is selling the same infinite feed with calmer branding.</p>

%s

    <h2>Questions</h2>
%s

%s
""" % (cn_stores(), faq_html(faqs_b), up)
    t = parent_trail + [(CN_SUBPAGES[1][0], "How to stop doomscrolling")]
    page(CN_SUBPAGES[1][0],
         "How to stop doomscrolling &mdash; four things that work",
         "Doomscrolling is an arrangement problem, not a willpower problem. Read a finite set, once a day, out of the bedroom, without notifications &mdash; and what an app can and cannot enforce.",
         "/assets/og/cn-doomscrolling.png", body_b, trail=t,
         extra_ld=[faq_ld(faqs_b)], current="/products/")

    # ---- how-to-<job>, second intent -----------------------------------
    faqs_c = [
        ("Is biased language the same as fake news?",
         "No, and conflating them is a good way to end up trusting nothing. Most emotionally loaded reporting is factually accurate. The adjectives are added to make an accurate story land harder, which is a separate problem from a story being untrue and has a much simpler fix: read past them."),
        ("Does reading several sources fix it?",
         "It fixes factual gaps and does very little for emotional loading, because the technique is close to universal across the spectrum. Two outlets that disagree about everything will both describe the thing they dislike using words chosen to provoke."),
        ("Can software remove bias?",
         "It can remove a specific, mechanical part of it &mdash; the evaluative adjectives and adverbs around the facts. It cannot fix which stories were chosen, which quotes were used or what was left out, and any product claiming it has solved bias has replaced a visible slant with an invisible one."),
    ]
    body_c = """    <div class="hero">
      <h1>How to read the news without getting angry</h1>
      <p class="lede lede-wide">The anger is a writing technique before it is a reaction.</p>
    </div>

    <div class="answer">
      <p>Most of what makes a news story infuriating is not the event. It is the roughly six words wrapped around the event by someone whose headline is competing against forty others for the same tap. Learn to see those six words and a large share of the anger goes with them.</p>
    </div>

    <h2>The adjective test</h2>
    <p>Take any headline that has just annoyed you and remove every adjective and adverb. &ldquo;Officials quietly slip controversial rule into sweeping new package&rdquo; becomes &ldquo;officials added a rule to a package.&rdquo; The second version is what happened. The first version is what happened plus an instruction about how to feel about it, and the instruction was written by someone who does not know you.</p>
    <p>Do this five times and it becomes automatic. It is the highest-yield reading habit I know of, and it costs nothing.</p>

    <h2>Watch for the verbs of conflict</h2>
    <p>Slams, blasts, hits out, erupts, sparks fury. These describe almost nothing &mdash; in practice they mean &ldquo;said,&rdquo; or occasionally &ldquo;posted.&rdquo; They exist to convert a statement into a fight, because a fight gets read. When you see one, mentally substitute &ldquo;said&rdquo; and check whether the story survives. Frequently there was no story.</p>

    <h2>Notice what the quote is doing</h2>
    <p>A quote from a named official is evidence. A quote from an anonymous critic, or a screenshot of a stranger being wrong, is not reporting on an event &mdash; it is an invitation to be angry at a person, selected from millions specifically for being the most provoking available. Nothing is learned from it. This is the category where the anger has the least to show for it.</p>

    <h2>Then change when you read</h2>
    <p>Anger about an event decays; anger that is refreshed every ninety minutes does not. Reading once, in a defined session, lets the decay happen. Checking repeatedly through the day keeps resetting it, which is why people can feel furious all week about something they only actually learned once.</p>

    <h2>What Calmly News does about it</h2>
    <p>It runs a version of the adjective test on the summaries automatically, so what arrives is closer to the stripped-down sentence than the theatrical one. It caps the day at ten stories, which handles the refresh problem. And it lets you filter keywords, for the subjects where the honest answer is that you are not in a position to read about it this month.</p>
    <p>What it does not do: it cannot fix which stories exist, which quotes were selected, or what was omitted. Those are editorial choices and no amount of processing recovers them. Removing the loaded adjectives is a real improvement and a partial one, and I would rather describe it as partial.</p>

%s

    <h2>Questions</h2>
%s

%s
""" % (cn_stores(), faq_html(faqs_c), up)
    t = parent_trail + [(CN_SUBPAGES[2][0], "How to read the news without getting angry")]
    page(CN_SUBPAGES[2][0],
         "How to read the news without getting angry &mdash; the adjective test",
         "Most news anger comes from the words around the facts, not the facts. The adjective test, the verbs of conflict, what a quote is doing, and why reading once a day matters.",
         "/assets/og/cn-angry.png", body_c, trail=t,
         extra_ld=[faq_ld(faqs_c)], current="/products/")


# --------------------------------------------------------------------------
# case studies, now under Sai Studio. The old /case-studies/ URLs stay live as
# redirect stubs -- nothing is deleted.
# --------------------------------------------------------------------------

CASE_STUDIES = [
    dict(slug="bible-project",
         title="Follow the breadcrumb: micro innovation on a proven genre",
         blurb="A better Bible reader in four weeks, by adding one thing to a genre that already worked.",
         desc="How a three-person team shipped a Bible reader with AI verse explanations in four weeks, by taking a proven genre and changing one thing about it.",
         og="/assets/og/case-bible.png"),
    dict(slug="web3-social-network",
         title="Build a production level social network in 4 weeks",
         blurb="A vertical-community social network, built to production standard on a four-week structure.",
         desc="Building a production-grade social network for a vertical community in four weeks, using a fixed weekly structure to keep scope honest.",
         og="/assets/og/case-web3.png"),
]


def fix_inline_images(body):
    """Give every ported image real width/height and drop the inline styles."""
    def repl(m):
        tag = m.group(0)
        src = re.search(r'src="([^"]+)"', tag).group(1)
        alt_m = re.search(r'alt="([^"]*)"', tag)
        alt = alt_m.group(1) if alt_m else ""
        w, h = dims(src)
        size = ' width="%d" height="%d"' % (w, h) if w else ""
        return ('<img src="%s" alt="%s"%s loading="lazy" decoding="async" '
                'style="border-radius:10px;margin:1.25rem 0;display:block">' % (src, alt, size))
    return re.sub(r"<img\b[^>]*>", repl, body)


def build_case_studies():
    base = "/sai-studio/case-studies/"
    trail0 = [("/", "Home"), ("/sai-studio/", "Sai Studio"), (base, "Case studies")]

    rows = "\n".join(
        '      <li><a href="%s%s/">%s<span class="sub-line">%s</span></a></li>'
        % (base, c["slug"], esc(c["title"]), esc(c["blurb"])) for c in CASE_STUDIES)
    body = """    <div class="hero">
      <h1>Case studies</h1>
      <p class="lede lede-wide">Client and partner builds delivered through <a href="/sai-studio/">Sai Studio</a>, written up as what was decided and why rather than as a highlight reel.</p>
    </div>

    <ul class="subpages">
%s
    </ul>

    <p class="section-note">These moved here from <code>/case-studies/</code> in August 2026. The old URLs still resolve and point at these pages.</p>
""" % rows
    page(base, "Case studies &mdash; Sai Studio",
         "Client and partner builds delivered through Sai Studio: a Bible reader with AI verse explanations, and a production social network, both on four-week structures.",
         "/assets/og/case-studies.png", body, trail=trail0, current="")

    for c in CASE_STUDIES:
        path = base + c["slug"] + "/"
        with open(os.path.join(ROOT, "_content/case-studies/%s.html" % c["slug"])) as f:
            content = fix_inline_images(f.read())
        t = trail0 + [(path, c["title"])]
        article_ld = """{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": %s,
  "description": %s,
  "image": "%s",
  "mainEntityOfPage": { "@type": "WebPage", "@id": "%s" },
  "author": { "@id": "%s/about/#person" },
  "publisher": { "@id": "%s/#website" },
  "inLanguage": "en"
}""" % (_json_str(c["title"]), _json_str(c["desc"]), SITE + c["og"], SITE + path, SITE, SITE)
        body = """    <div class="hero">
      <h1>%s</h1>
      <p class="lede lede-wide">%s</p>
    </div>

%s

    <hr>
    <p><a href="%s">&larr; All case studies</a> &middot; <a href="/sai-studio/">Sai Studio</a></p>
""" % (esc(c["title"]), esc(c["blurb"]), content, base)
        page(path, c["title"] + " &mdash; Sai Studio", c["desc"], c["og"],
             body, trail=t, extra_ld=[article_ld], current="")


REDIRECTS = [
    ("/case-studies/", "/sai-studio/case-studies/"),
    ("/case-studies/bible-project/", "/sai-studio/case-studies/bible-project/"),
    ("/case-studies/web3-social-network/", "/sai-studio/case-studies/web3-social-network/"),
]


def build_redirects():
    for old, new in REDIRECTS:
        doc = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Moved &mdash; Sai vs. Reality</title>
  <meta name="robots" content="noindex, follow">
  <link rel="canonical" href="%(site)s%(new)s">
  <meta http-equiv="refresh" content="0; url=%(new)s">
  <link rel="stylesheet" href="/assets/css/site.css">
</head>
<body>
  <main id="main" class="wrap">
    <div class="hero">
      <h1>This page moved</h1>
      <p class="lede">Case studies now live under Sai Studio.</p>
      <p><a class="btn" href="%(new)s">Continue &rarr;</a></p>
    </div>
  </main>
  <script>location.replace(%(newjs)s);</script>
</body>
</html>
""" % dict(site=SITE, new=new, newjs='"%s"' % new)
        rel = old.lstrip("/") + "index.html"
        dest = os.path.join(ROOT, rel)
        if not os.path.isdir(os.path.dirname(dest)):
            os.makedirs(os.path.dirname(dest))
        with open(dest, "w") as f:
            f.write(doc)


# --------------------------------------------------------------------------
# the hand-built landing pages
# --------------------------------------------------------------------------

def add_image_dims(rel):
    """Give every local <img> in a hand-built page real width/height (CLS).
    Idempotent: images that already declare a size are left alone."""
    src = os.path.join(ROOT, rel)
    with open(src) as f:
        t = f.read()
    base = "/" + os.path.dirname(rel)

    def repl(m):
        tag = m.group(0)
        if "width=" in tag:
            return tag
        u = re.search(r'src="([^"]+)"', tag)
        if not u or u.group(1).startswith(("http", "data:")):
            return tag
        path = u.group(1)
        look = path if path.startswith("/") else base + "/" + path
        w, h = dims(look)
        if not w:
            return tag
        extra = ' width="%d" height="%d"' % (w, h)
        if "loading=" not in tag:
            extra += ' loading="lazy" decoding="async"'
        return tag[:-1].rstrip() + extra + ">"

    t2 = re.sub(r"<img\b[^>]*>", repl, t)
    if t2 != t:
        with open(src, "w") as f:
            f.write(t2)


MAIN_OPEN = "<!-- svr:main:open -->"
MAIN_CLOSE = "<!-- svr:main:close -->"


def pin_light(rel):
    """Sai Studio, Chatengage and Founder's Note are fixed light designs that do
    not answer prefers-color-scheme. Pin the injected brand strip to the light
    palette on those pages so it cannot go dark against a white page."""
    src = os.path.join(ROOT, rel)
    with open(src) as f:
        t = f.read()
    if 'data-theme="light"' in t:
        return
    t = re.sub(r"<html\b([^>]*)>", lambda m: '<html%s data-theme="light">' % m.group(1), t, count=1)
    with open(src, "w") as f:
        f.write(t)


def ensure_main(rel):
    """Give a hand-built page a single <main> landmark, if it has none.
    Opens just after the injected brand strip and closes before <footer>."""
    src = os.path.join(ROOT, rel)
    with open(src) as f:
        t = f.read()
    if MAIN_OPEN in t or re.search(r"<main\b", t):
        return
    at = t.index(BODY_END) + len(BODY_END)
    t = t[:at] + '\n%s\n<main id="main">\n' % MAIN_OPEN + t[at:]
    m = re.search(r"<footer\b", t)
    t = t[:m.start()] + "</main>\n%s\n" % MAIN_CLOSE + t[m.start():]
    with open(src, "w") as f:
        f.write(t)


def build_landing_pages():
    home = [("/", "Home")]
    prods = [("/", "Home"), ("/products/", "Products")]

    # ---- Sai Studio (live product; a service, so Service not SoftwareApplication)
    service_ld = """{
  "@context": "https://schema.org",
  "@type": "Service",
  "@id": "%(site)s/sai-studio/#service",
  "name": "Sai Studio",
  "url": "%(site)s/sai-studio/",
  "serviceType": "MVP development for non-technical founders",
  "description": "CTO-level strategy and a fixed-scope first build for founders who do not have a technical co-founder, without taking equity.",
  "provider": { "@id": "%(site)s/about/#person" },
  "areaServed": "Worldwide",
  "inLanguage": "en"
}""" % dict(site=SITE)
    retrofit("sai-studio/index.html",
             "Sai Studio &mdash; MVP builds for founders without a technical co-founder",
             "CTO-level strategy and a fixed-scope first build, without giving away equity. Case studies from four-week builds, and what the process actually involves.",
             "/assets/og/sai-studio.png",
             prods + [("/sai-studio/", "Sai Studio")],
             extra_ld=[service_ld],
             tail="""  <div class="wrap">
    <h2>Case studies</h2>
    <p>Full write-ups of builds delivered through Sai Studio.</p>
    <ul class="subpages">
      <li><a href="/sai-studio/case-studies/bible-project/">Follow the breadcrumb: micro innovation on a proven genre<span class="sub-line">A better Bible reader in four weeks, by adding one thing to a genre that already worked.</span></a></li>
      <li><a href="/sai-studio/case-studies/web3-social-network/">Build a production level social network in 4 weeks<span class="sub-line">A vertical-community social network, built to production standard on a four-week structure.</span></a></li>
    </ul>
  </div>""")

    # ---- Chatengage (building)
    ce_ld = """{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "@id": "%(site)s/chatengage/#app",
  "name": "Chatengage",
  "url": "%(site)s/chatengage/",
  "applicationCategory": "BusinessApplication",
  "operatingSystem": "Web browser",
  "description": "Share documents, video or a landing page as one package with a chatbot that answers questions about it and captures what comes back.",
  "author": { "@id": "%(site)s/about/#person" },
  "inLanguage": "en"
}""" % dict(site=SITE)
    retrofit("chatengage/index.html",
             "Chatengage &mdash; send documents as a package that answers questions",
             "Bundle documents, video or a landing page into one shareable package with a bot that guides the recipient, answers their questions and captures the feedback. In development.",
             "/assets/og/chatengage.png",
             prods + [("/chatengage/", "Chatengage")],
             extra_ld=[ce_ld],
             banner="""  <div class="wrap">
    <div class="callout">
      <p><strong>Chatengage is still being built.</strong> %s Everything below is what it is meant to be, written before Reality has had its say. If it turns out to be wrong, that will be published here too.</p>
    </div>
  </div>""" % status_pill("building"))

    # ---- Founder's Note (killed)
    fn = BY_SLUG["founders-note"]
    # No SoftwareApplication here: the product was never built, and emitting
    # app markup for software that does not exist is a lie to a crawler.
    fn_ld = """{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Founder's Note: killed during ideation",
  "description": "Why Founder's Note was stopped before it was built: founders recognised the context-switching cost and would not pay to remove it.",
  "mainEntityOfPage": { "@type": "WebPage", "@id": "%(site)s/founders-note/" },
  "author": { "@id": "%(site)s/about/#person" },
  "publisher": { "@id": "%(site)s/#website" },
  "inLanguage": "en"
}""" % dict(site=SITE)
    retrofit("founders-note/index.html",
             "Founder's Note &mdash; killed, with the post-mortem",
             "Founder's Note was a context-first founder workspace built around one agent with the whole company in memory. It is discontinued. The page stays up, with a post-mortem.",
             "/assets/og/founders-note.png",
             prods + [("/founders-note/", "Founder's Note")],
             extra_ld=[fn_ld],
             banner=killed_banner(fn),
             tail="""  <div class="wrap">
    <h2 id="post-mortem">Post-mortem</h2>
    <p class="section-note">Killed products keep their URL here and gain this instead of a redirect.</p>
%s
    <p><a href="/killed/">Other killed products &rarr;</a></p>
  </div>""" % pm_dl("founders-note"))

    # ---- Partnership page: kept live, given a head and a link so it is not
    # ---- orphaned now that the homepage is a product index.
    retrofit("partners/unicornio-macau/index.html",
             "Partnership with Unicornio Macau Ltd",
             "A publishing partnership with Unicornio Macau Ltd, combining app development with business development and go-to-market.",
             "/assets/og/products.png",
             home + [("/partners/unicornio-macau/", "Unicornio Macau")])

    # ---- Field notes (private project, kept live but deliberately low key)
    retrofit("field-notes/index.html",
             "Vancouver Field Notes &mdash; Sai &times; Jay",
             "A private journal of Vancouver coffee, food and neighbourhoods, kept between two friends. Not a product and not a ranking.",
             "/assets/og/field-notes.png",
             home + [("/field-notes/", "Field notes")],
             noindex=True,
             banner="""  <div class="wrap">
    <div class="callout">
      <p class="section-note">A private side project between two friends, kept here for convenience. Not a product, not maintained to any standard, and not indexed.</p>
    </div>
  </div>""")


# --------------------------------------------------------------------------
# robots, sitemaps, 404
# --------------------------------------------------------------------------

PRODUCT_SITEMAPS = [
    "/products/bible-project/sitemap.xml",
    "/products/canieat/sitemap.xml",
    "/products/flexi/sitemap.xml",
    "/products/pool-billiards-self-trainer/sitemap.xml",
    "/products/runout-rank/sitemap.xml",
    "/products/snooker-self-trainer/sitemap.xml",
    "/products/tacet/sitemap.xml",
]

NOINDEX = set(["/field-notes/"])


def sitemap_lastmod(rel):
    p = os.path.join(ROOT, rel.lstrip("/"))
    if not os.path.exists(p):
        return TODAY
    with open(p) as f:
        found = re.findall(r"<lastmod>([0-9]{4}-[0-9]{2}-[0-9]{2})", f.read())
    return max(found) if found else TODAY


def build_sitemaps():
    urls = sorted(set(p for p in PAGES if p not in NOINDEX))
    if not BUILD_LOG:
        urls = [u for u in urls if u != "/build-log/"]
    entries = "\n".join(
        "  <url><loc>%s%s</loc><lastmod>%s</lastmod></url>" % (SITE, u, TODAY) for u in urls)
    with open(os.path.join(ROOT, "sitemap-pages.xml"), "w") as f:
        f.write("""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
%s
</urlset>
""" % entries)

    idx = ['  <sitemap><loc>%s/sitemap-pages.xml</loc><lastmod>%s</lastmod></sitemap>' % (SITE, TODAY)]
    for s in PRODUCT_SITEMAPS:
        idx.append('  <sitemap><loc>%s%s</loc><lastmod>%s</lastmod></sitemap>'
                   % (SITE, s, sitemap_lastmod(s)))
    with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
        f.write("""<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
%s
</sitemapindex>
""" % "\n".join(idx))

    with open(os.path.join(ROOT, "robots.txt"), "w") as f:
        f.write("""# Only the robots.txt at the origin root is honoured, so every sitemap on this
# domain -- including the ones inside each product submodule -- is listed here.
User-agent: *
Allow: /
Disallow: /products/flexi/src/
Disallow: /products/bible-project/_data/

Sitemap: %s/sitemap.xml
%s
""" % (SITE, "\n".join("Sitemap: %s%s" % (SITE, s) for s in PRODUCT_SITEMAPS)))


def build_404():
    body = """    <div class="hero">
      <h1>404</h1>
      <p class="lede">This page does not exist. Nothing here has been deleted or redirected on purpose, so this is most likely a typo or a link I broke.</p>
    </div>
    <ul class="subpages">
      <li><a href="/products/">All products<span class="sub-line">Everything shipped, building, or killed.</span></a></li>
      <li><a href="/killed/">Killed products<span class="sub-line">The post-mortems. These keep their URLs forever.</span></a></li>
    </ul>
"""
    doc_path = "/404.html"
    page(doc_path, "Page not found &mdash; Sai vs. Reality",
         "That page does not exist on this site.", "/assets/og/home.png",
         body, noindex=True)
    PAGES.remove(doc_path)


def main():
    build_home()
    build_products_index()
    build_killed_index()
    build_about()
    build_build_log()
    build_calmly_news()
    build_harness_survey()
    build_case_studies()
    build_landing_pages()
    for rel in ("sai-studio/index.html", "chatengage/index.html",
                "founders-note/index.html", "partners/unicornio-macau/index.html"):
        pin_light(rel)
    ensure_main("sai-studio/index.html")
    for rel in ("sai-studio/index.html", "chatengage/index.html",
                "founders-note/index.html", "field-notes/index.html",
                "partners/unicornio-macau/index.html"):
        add_image_dims(rel)
    build_redirects()
    build_404()
    build_sitemaps()
    print("built %d pages" % len(PAGES))
    for p in sorted(set(PAGES)):
        print("  ", p)


if __name__ == "__main__":
    main()
