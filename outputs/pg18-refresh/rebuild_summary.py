"""Rebuild SUMMARY.md hierarchy from PostgreSQL 18 upstream navigation."""
from pathlib import Path
import os
import re
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HTML = Path(tempfile.gettempdir()) / "postgresql-18.6-docs" / "postgresql-18.6" / "doc" / "src" / "sgml" / "html"

entries = []
for line in (ROOT / "SUMMARY.md").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^\s*\* \[(.+)\]\(([^)]+)\)$", line)
    if m:
        entries.append({"title": m.group(1), "path": m.group(2)})

by_page = {}
for entry in entries:
    text = (ROOT / entry["path"]).read_text(encoding="utf-8")
    source = re.search(r"https://www\.postgresql\.org/docs/18/([^/]+\.html)", text)
    if source:
        by_page[source.group(1)] = entry

parents = {}
next_pages = {}
for page, entry in by_page.items():
    raw = (HTML / page).read_text(encoding="utf-8")
    up = re.search(r'<a\s+accesskey="u"\s+href="([^"#]+\.html)"', raw)
    parents[page] = up.group(1) if up and up.group(1) in by_page else None
    next_link = re.search(r'<link\s+rel="next"\s+href="([^"#]+\.html)"', raw)
    next_pages[page] = next_link.group(1) if next_link and next_link.group(1) in by_page else None

order = {}
page = "index.html"
while page in by_page and page not in order:
    order[page] = len(order)
    page = next_pages.get(page)

ROMAN = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7, "VIII": 8}
def order_key(page):
    title = by_page[page]["title"]
    if by_page[page]["path"] == "README.md":
        return (-3,)
    if title == "Preface":
        return (-2,)
    if title == "Bibliography":
        return (99,)
    m = re.match(r"Part ([IVX]+)\.", title)
    if m:
        return (-1, ROMAN.get(m.group(1), 99))
    m = re.match(r"Chapter (\d+)\.", title)
    if m:
        return (0, int(m.group(1)))
    m = re.match(r"Appendix ([A-Z])\.", title)
    if m:
        return (0, ord(m.group(1)))
    m = re.match(r"([A-Z]|\d+)(?:\.(\d+))*\.", title)
    if m:
        parts = re.findall(r"\d+", m.group(0))
        first = ord(m.group(1)) if m.group(1).isalpha() else int(m.group(1))
        return (1, first, *(int(n) for n in parts), title.lower())
    return (2, order.get(page, len(order)), by_page[page]["path"])

children = {page: [] for page in by_page}
roots = []
for page, parent in parents.items():
    if parent:
        children[parent].append(page)
    else:
        roots.append(page)
for group in children.values():
    group.sort(key=order_key)
roots.sort(key=order_key)

lines = ["# Table of contents", ""]
emitted = set()
def emit(page, depth, ancestors=()):
    if page in ancestors:
        raise RuntimeError("navigation cycle: " + " -> ".join(ancestors + (page,)))
    if page in emitted:
        return
    emitted.add(page)
    entry = by_page[page]
    lines.append("  " * depth + f'* [{entry["title"]}]({entry["path"]})')
    for child in children[page]:
        emit(child, depth + 1, ancestors + (page,))

for page in roots:
    emit(page, 0)
if len(emitted) != len(by_page):
    raise RuntimeError(f"unemitted pages: {len(by_page) - len(emitted)}")
(ROOT / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"entries={len(entries)} source_pages={len(by_page)} roots={len(roots)}")
