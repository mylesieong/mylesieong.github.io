#!/usr/bin/env python3
"""Link, orphan and per-page SEO check for the hub. `python3 check.py`"""
import os, re, glob, json
from urllib.parse import urlparse, unquote

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
SKIP_DIRS = ('_site/', '_content/')
# build inputs served but never linked; excluded from crawl and orphan checks
TEMPLATES = ('products/flexi/src/', 'products/bible-project/_data/')
# files that are intentionally unlinked
EXEMPT = ('404.html', 'googlef3c32cf8dc998f2f.html', 'privacy-policy.html')

files = [f for f in glob.glob('**/*.html', recursive=True) if not f.startswith(SKIP_DIRS)]
href = re.compile(r'(?:href|src)="([^"]+)"')


def resolve(f, u):
    p = unquote(urlparse(u).path)
    if not p:
        return None
    tgt = p.lstrip('/') if p.startswith('/') else os.path.normpath(os.path.join(os.path.dirname(f), p))
    if tgt in ('', '.'):
        tgt = 'index.html'
    return os.path.join(tgt, 'index.html') if os.path.isdir(tgt) else tgt


broken, linked, redirects = [], set(), set()
for f in files:
    if f.startswith(TEMPLATES):
        continue
    t = open(f, encoding='utf-8', errors='ignore').read()
    if 'http-equiv="refresh"' in t:
        redirects.add(os.path.normpath(f))
    for u in href.findall(t):
        if u.startswith(('http', 'mailto:', '#', 'data:', 'javascript:', '//')):
            continue
        c = resolve(f, u)
        if c is None:
            continue
        if not os.path.exists(c):
            broken.append((f, u))
        elif c.endswith('.html'):
            linked.add(os.path.normpath(c))

print("broken internal links: %d" % len(broken))
for f, u in broken:
    print("   %s -> %s" % (f, u))

orph = [f for f in files
        if os.path.normpath(f) not in linked
        and os.path.normpath(f) not in redirects
        and not f.endswith(EXEMPT)
        and not f.startswith(TEMPLATES)
        and not re.search(r'/(zh|ko|vi|pt)/', f)]
print("\norphan pages: %d" % len(orph))
for f in sorted(orph):
    print("   %s" % f)

print("\nper-page checks (hub pages only):")
hub = [f for f in files
       if not f.startswith('products/')
       or f.startswith(('products/index', 'products/calmly-news', 'products/harness-survey'))]
fails = 0
for f in sorted(hub):
    if f.endswith('googlef3c32cf8dc998f2f.html'):
        continue
    t = open(f, encoding='utf-8', errors='ignore').read()
    if 'http-equiv="refresh"' in t:
        continue
    probs = []
    if len(re.findall(r'<h1[^>]*>', t)) != 1:
        probs.append("h1 count != 1")
    for need, label in (('rel="canonical"', 'canonical'), ('og:image', 'og:image'),
                        ('twitter:card', 'twitter card'),
                        ('<meta name="description"', 'description')):
        if need not in t:
            probs.append("no " + label)
    lv = [int(m) for m in re.findall(r'<h([1-6])[^>]*>', t)]
    for a, b in zip(lv, lv[1:]):
        if b > a + 1:
            probs.append("heading jump h%d->h%d" % (a, b))
            break
    for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
        try:
            json.loads(m)
        except Exception as e:
            probs.append("invalid JSON-LD: %s" % e)
    noWH = [i for i in re.findall(r'<img\b[^>]*>', t)
            if 'width=' not in i and not re.search(r'src="(https?:|data:)', i)]
    if noWH:
        probs.append("%d img without width/height" % len(noWH))
    if probs:
        fails += 1
    print("   %-4s %s%s" % ("FAIL" if probs else "ok", f, "  :: " + "; ".join(probs) if probs else ""))

print("\n%d page(s) with problems, %d broken link(s), %d orphan(s)" % (fails, len(broken), len(orph)))
