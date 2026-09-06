"""Build a PostgreSQL 18 GitBook source tree from the official HTML archive.

The source archive is PostgreSQL 18.6, retrieved 2026-09-06.  This script
uses upstream HTML slugs for all file and directory names, so paths contain no
chapter or section numbers.  It builds into TEMP first; `apply` is separate.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path
from urllib.parse import unquote, urlsplit

TOOLS = Path(__file__).resolve().parents[1] / ".tools" / "pg18-doc-tools"
sys.path.insert(0, str(TOOLS))
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
HTML = Path(tempfile.gettempdir()) / "postgresql-18.6-docs" / "postgresql-18.6" / "doc" / "src" / "sgml" / "html"
STAGE = Path(tempfile.gettempdir()) / "pgsql-tw-pg18-stage"
BASE = "https://www.postgresql.org/docs/18/"

PARTS = {
    "tutorial.html": "tutorial",
    "sql.html": "the-sql-language",
    "admin.html": "server-administration",
    "client-interfaces.html": "client-interfaces",
    "server-programming.html": "server-programming",
    "reference.html": "reference",
    "internals.html": "internals",
    "appendixes.html": "appendixes",
}
SKIP = {"bookindex.html", "legalnotice.html"}

def soup(page: str):
    return BeautifulSoup((HTML / page).read_text(encoding="utf-8"), "html.parser")

def title_of(doc):
    main = doc.select_one("#docContent > div:not(.navheader):not(.navfooter)")
    if main is None:
        raise ValueError("no main content")
    h = main.find(re.compile(r"^h[1-6]$"))
    if h is None:
        raise ValueError("no heading")
    return main, " ".join(h.get_text(" ", strip=True).split())

def links(doc, rel):
    x = next((tag for tag in doc.find_all("link") if rel in (tag.get("rel") or [])), None)
    if x is None and rel == "up":
        x = doc.find("a", attrs={"accesskey": "u"})
    return x.get("href") if x and x.get("href", "").endswith(".html") else None

def inventory():
    nodes = {}
    for f in HTML.glob("*.html"):
        page = f.name
        if page in SKIP:
            continue
        try:
            doc = soup(page)
            main, title = title_of(doc)
        except ValueError:
            continue
        parent = links(doc, "up")
        nodes[page] = {"page": page, "title": title, "parent": parent}
    # Keep only pages attached to the manual root via upstream navigation.
    def rooted(page, seen=()):
        if page in seen:
            return False
        parent = nodes[page]["parent"]
        return page == "index.html" or parent == "index.html" or (parent in nodes and rooted(parent, seen + (page,)))
    nodes = {p: n for p, n in nodes.items() if rooted(p)}
    for n in nodes.values():
        if n["parent"] not in nodes:
            n["parent"] = None
    return nodes

def root_part(page, nodes):
    p = page
    while nodes[p]["parent"] and nodes[p]["parent"] != "index.html":
        p = nodes[p]["parent"]
    return p

def path_for(page, nodes):
    if page == "index.html":
        return Path("README.md")
    if page == "preface.html":
        return Path("preface/README.md")
    if page == "biblio.html":
        return Path("bibliography.md")
    root = root_part(page, nodes)
    if root in PARTS:
        base = Path(PARTS[root])
        if page == root:
            return base / "README.md"
        # The direct child of a Part owns a directory; all of its descendants
        # stay together in that chapter directory.
        first = page
        while nodes[first]["parent"] != root:
            first = nodes[first]["parent"]
        if page == first:
            return base / first.removesuffix(".html") / "README.md"
        return base / first.removesuffix(".html") / (page.removesuffix(".html") + ".md")
    # Preface sections and other root-attached pages.
    return Path("preface") / (page.removesuffix(".html") + ".md")

class Converter(MarkdownConverter):
    def convert_pre(self, el, text, parent_tags):
        raw = el.get_text().rstrip("\n")
        ticks = "`" * max(3, max((len(s) for s in re.findall(r"`+", raw)), default=0) + 1)
        return f"\n\n{ticks}\n{raw}\n{ticks}\n\n"
    def convert_table(self, el, text, parent_tags):
        return "\n\n" + str(el) + "\n\n"
    def convert_a(self, el, text, parent_tags):
        if not el.get("href") and (el.get("id") or el.get("name")):
            return f'<a id="{el.get("id") or el.get("name")}"></a>' + text
        return super().convert_a(el, text, parent_tags)
    def convert_br(self, el, text, parent_tags):
        return "<br>"

def page_markdown(page, node, nodes):
    doc = soup(page)
    main, _ = title_of(doc)
    for n in main.select(".navheader, .navfooter"):
        n.decompose()
    # Preserve source anchors independently of element classes.
    for tag in list(main.find_all(id=True)):
        if tag.name == "a" or tag.find_parent("table"):
            continue
        anchor = doc.new_tag("a", id=tag["id"])
        del tag["id"]
        tag.insert_before(anchor)
    for a in main.find_all("a", href=True):
        u = urlsplit(a["href"])
        target = Path(unquote(u.path)).name
        if not u.scheme and target in nodes:
            rel = os.path.relpath(path_for(target, nodes), path_for(page, nodes).parent).replace("\\", "/")
            a["href"] = rel + (("#" + u.fragment) if u.fragment else "")
        elif not u.scheme and u.path:
            a["href"] = BASE + a["href"]
        a.attrs.pop("title", None)
    for img in main.find_all("img", src=True):
        if not urlsplit(img["src"]).scheme:
            img["src"] = BASE + img["src"]
    md = Converter(heading_style="ATX", bullets="*", escape_underscores=False, wrap=False).convert(str(main)).strip()
    return md + "\n\n---\n\n原文：[PostgreSQL 18.6 Documentation](" + BASE + page + ")（英文原文，待翻譯）\n"

def build():
    if not HTML.is_dir():
        raise SystemExit(f"Archive not found: {HTML}")
    nodes = inventory()
    paths = {}
    for page in nodes:
        path = path_for(page, nodes).as_posix()
        if path in paths:
            raise SystemExit(f"path collision: {page} and {paths[path]} -> {path}")
        paths[path] = page
        nodes[page]["path"] = path
    if STAGE.exists():
        shutil.rmtree(STAGE)
    STAGE.mkdir()
    for page, node in nodes.items():
        target = STAGE / node["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page_markdown(page, node, nodes), encoding="utf-8")
    lines = ["# Table of contents", ""]
    # The source tree retains upstream parent relations in its directories.
    # A flat, path-sorted summary avoids treating generated cross-reference
    # navigation as a hierarchy edge.
    for p in sorted(nodes, key=lambda p: nodes[p]["path"]):
        n = nodes[p]
        lines.append(f'* [{n["title"]}]({n["path"]})')
    (STAGE / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    report = {"version": "18.6", "retrieved": "2026-09-06", "source": BASE,
              "pages": len(nodes), "stage": str(STAGE),
              "paths": sorted(paths), "summary_entries": len(nodes)}
    (OUT / "plan.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] != "build":
        raise SystemExit("Usage: import_manual.py build")
    build()
