#!/usr/bin/env python3
import re, sys, time, urllib.request
from xml.etree import ElementTree as ET

BASE = "https://scicom.ucsc.edu"
PATTERN = re.compile(
    r'https?://(?:www\.)?(?:ucscsciencenotes\.com|sciencenotes\.ucsc\.edu)[^\s"\'<>)]*', re.I)
UA = {"User-Agent": "Mozilla/5.0 (link check by site staff)"}
NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}loc"

def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return r.read().decode("utf-8", "replace")

def from_sitemap(url):
    try:
        root = ET.fromstring(get(url))
    except Exception:
        return []
    out = []
    for loc in root.iter(NS):
        u = loc.text.strip()
        out += from_sitemap(u) if u.endswith(".xml") else [u]
    return out

pages = []
for path in ("/wp-sitemap.xml", "/sitemap.xml", "/sitemap_index.xml"):
    pages = from_sitemap(BASE + path)
    if pages:
        break
pages = sorted(set(pages) | {BASE + "/"})
print(len(pages), "pages to check", file=sys.stderr)

for i, u in enumerate(pages, 1):
    try:
        html = get(u)
    except Exception as e:
        print("ERROR", u, e)
        continue
    hits = sorted(set(PATTERN.findall(html)))
    if hits:
        print("FOUND", u, hits, flush=True)
    if i % 50 == 0:
        print(f"...{i}/{len(pages)}", file=sys.stderr)
    time.sleep(0.5)
