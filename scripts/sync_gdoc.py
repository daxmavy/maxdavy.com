#!/usr/bin/env python3
"""Refresh pages whose text lives in a Google Doc.

A page opts in with a `gdoc: <document id>` line in its front matter. The first
line of the document becomes the page title; everything after it replaces the
page body, unchanged. All other front matter is kept.

The document must be readable by anyone with the link.

Usage: python3 scripts/sync_gdoc.py [content-dir]
Exits 1 if any document could not be fetched; those pages keep their old text.
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

EXPORT_URL = "https://docs.google.com/document/d/{doc}/export?format=md"
FRONT_MATTER = re.compile(r"\A---\n(.*?\n)---\n", re.DOTALL)


def fetch_export(doc):
    with urllib.request.urlopen(EXPORT_URL.format(doc=doc), timeout=60) as response:
        return response.read().decode("utf-8")


def split_export(export):
    title, _, body = export.lstrip("﻿\n").partition("\n")
    body = body.lstrip("\n")
    if not title.strip() or not body.strip():
        raise ValueError("document has no title line or no body")
    return title.strip(), body.rstrip("\n") + "\n"


def doc_id(page):
    front = FRONT_MATTER.match(page)
    found = front and re.search(r"^gdoc:\s*(\S+)\s*$", front.group(1), re.MULTILINE)
    return found.group(1) if found else None


def render_page(page, export):
    title, body = split_export(export)
    front = FRONT_MATTER.match(page).group(1)
    front = re.sub(
        r"^title:.*$", lambda _: "title: " + json.dumps(title, ensure_ascii=False),
        front, count=1, flags=re.MULTILINE,
    )
    return f"---\n{front}---\n{body}"


def sync_all(content_dir, fetch=fetch_export):
    failed = []
    for path in sorted(Path(content_dir).rglob("*.md")):
        page = path.read_text(encoding="utf-8")
        doc = doc_id(page)
        if not doc:
            continue
        try:
            path.write_text(render_page(page, fetch(doc)), encoding="utf-8")
            print(f"synced {path}")
        except (OSError, ValueError) as error:
            print(f"FAILED {path}: {error}", file=sys.stderr)
            failed.append(path)
    return failed


if __name__ == "__main__":
    sys.exit(1 if sync_all(sys.argv[1] if len(sys.argv) > 1 else "content") else 0)
