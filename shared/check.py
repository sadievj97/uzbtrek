#!/usr/bin/env python3
"""Site checker. Usage: python3 check.py SITE_DIR [SITE_DIR ...]

For each site directory (its *.html files, not recursive) it reports:
  - photos used more than once anywhere in the site (rule: every photo appears once per site),
    including the same picture saved under two names (SAME_PHOTO)
  - referenced local files that do not exist (images, css, js)
  - internal links to pages that do not exist
  - banned text: em dashes, prices ($ followed by a digit), "TREK 2027", operator line, old copy that was removed
Exit code 1 if anything fails.
"""
import os, re, sys, html
from collections import Counter

IMG_RE = re.compile(r'''(?:src|href|data-src|data-bg)\s*=\s*["']([^"']+\.(?:webp|jpe?g|png|gif|avif))["']|url\(\s*["']?([^"')]+\.(?:webp|jpe?g|png|gif|avif))["']?\s*\)''', re.I)
ASSET_RE = re.compile(r'''(?:src|href)\s*=\s*["']([^"'#?]+\.(?:js|css|svg|webp|jpe?g|png))["']''', re.I)
LINK_RE = re.compile(r'''href\s*=\s*["']([^"']+)["']''', re.I)
# Different file names, same picture (exact copies or burst shots): never use two of a group on one site.
SAME_PHOTO = [("a000", "tashkent_painted_hall"), ("a131", "bukhara_panorama"), ("a308", "nowruz_trees_group"),
              ("a638", "mountains_charvak"), ("a070", "a072"), ("a410", "cohort_registan"), ("a709", "a710")]
BANNED = [
    ("em dash", re.compile("—|&mdash;")),
    ("price", re.compile(r"\$\s?\d")),
    ("side label with year", re.compile(r"TREK\s+2027")),
    ("operator line", re.compile(r"Operated by|license no\.", re.I)),
    ("removed copy: pays operator in gets list", re.compile(r"so you never collect money", re.I)),
    ("removed copy: movie night", re.compile(r"movie night", re.I)),
    ("removed copy: born in Samarkand", re.compile(r"(raised|born) in Samarkand|As a boy in Samarkand", re.I)),
    ("removed copy: Timeline for a March trek", re.compile(r"(?<!Example )Timeline for a March trek", re.I)),
]


def strip_scripts(text):
    return re.sub(r"<script\b[^>]*>.*?</script>", "", text, flags=re.S | re.I)


def check_site(site):
    problems = []
    pages = sorted(f for f in os.listdir(site) if f.endswith(".html"))
    uses = Counter()
    where = {}
    for page in pages:
        path = os.path.join(site, page)
        raw = open(path, encoding="utf-8").read()
        text = strip_scripts(raw)
        for m in IMG_RE.finditer(text):
            ref = m.group(1) or m.group(2)
            if ref.startswith(("data:", "http")):
                continue
            base = os.path.basename(ref)
            if base.startswith(("logo", "favicon", "pattern")):
                continue
            uses[base] += 1
            where.setdefault(base, []).append(page)
        for m in ASSET_RE.finditer(raw):
            ref = m.group(1)
            if ref.startswith(("http", "data:", "//", "mailto:", "tel:")):
                continue
            target = os.path.normpath(os.path.join(site, ref))
            if not os.path.exists(target):
                problems.append(f"{page}: missing file {ref}")
        for m in LINK_RE.finditer(text):
            ref = html.unescape(m.group(1))
            if ref.startswith(("http", "mailto:", "tel:", "#", "data:", "javascript:")):
                continue
            ref = ref.split("#")[0].split("?")[0]
            if not ref or not ref.endswith((".html", "/")):
                continue
            target = os.path.normpath(os.path.join(site, ref))
            if ref.endswith("/"):
                target = os.path.join(target, "index.html")
            if not os.path.exists(target):
                problems.append(f"{page}: broken link {m.group(1)}")
        visible = re.sub(r"<style\b[^>]*>.*?</style>", "", text, flags=re.S | re.I)
        for name, rx in BANNED:
            for mm in rx.finditer(visible):
                ctx = visible[max(0, mm.start() - 40): mm.end() + 40].replace("\n", " ")
                problems.append(f"{page}: {name}: ...{ctx}...")
    for base, n in uses.items():
        if n > 1:
            problems.append(f"photo used {n} times: {base} on {', '.join(where[base])}")
    stems = {os.path.splitext(b)[0]: b for b in uses}
    for group in SAME_PHOTO:
        hit = [g for g in group if g in stems]
        if len(hit) > 1:
            problems.append(f"same picture under two names: {', '.join(hit)}")
    return pages, uses, problems


def main():
    bad = False
    for site in sys.argv[1:]:
        pages, uses, problems = check_site(site)
        print(f"== {site}: {len(pages)} pages, {len(uses)} distinct photos")
        for p in problems:
            print("  FAIL", p)
        if not problems:
            print("  ok")
        bad = bad or bool(problems)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
