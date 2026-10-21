#!/usr/bin/env python3
"""Offline, stdlib-only checks of the two public HTML publications.

This validates the *publication's structure*, not historical Bitcoin claims,
source provenance, or third-party HTTP availability.
"""
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
PAGES = ("index.html", "proofs.html")


class AuditHTML(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.links: list[str] = []
        self.translations = 0
        self.missing_translation = 0
        self.images: list[dict[str, str]] = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.append(attrs["id"])
        if tag == "a" and "href" in attrs:
            self.links.append(attrs["href"])
        if tag == "img":
            self.images.append(attrs)
        has_fr = "data-fr" in attrs
        has_en = "data-en" in attrs
        if has_fr or has_en:
            self.translations += 1
            if not (has_fr and has_en):
                self.missing_translation += 1


def check_page(path: Path) -> list[str]:
    errors = []
    raw = path.read_text(encoding="utf-8")
    parsed = AuditHTML()
    parsed.feed(raw)
    parsed.close()
    ids = set(parsed.ids)
    if len(parsed.ids) != len(ids):
        errors.append("duplicate HTML id attributes")
    if parsed.missing_translation:
        errors.append(f"{parsed.missing_translation} unpaired FR/EN attributes")
    if not parsed.translations:
        errors.append("no bilingual data-fr/data-en entries")
    for href in parsed.links:
        parts = urlsplit(href)
        if parts.scheme or href.startswith("//") or parts.path.startswith("/"):
            continue
        target_path = (path.parent / unquote(parts.path)).resolve() if parts.path else path
        if not target_path.is_relative_to(ROOT.resolve()):
            errors.append(f"relative link outside repository: {href}")
        elif parts.path and not target_path.is_file():
            errors.append(f"missing local file: {href}")
        elif parts.fragment and target_path.is_file() and target_path.suffix.lower() in (".html", ".htm"):
            if target_path == path:
                target_ids = ids
            else:
                other = AuditHTML()
                other.feed(target_path.read_text(encoding="utf-8"))
                other.close()
                target_ids = set(other.ids)
            if unquote(parts.fragment) not in target_ids:
                errors.append(f"missing local or cross-page anchor: {href}")
    if "C:\\Users\\" in raw or "E:\\Selma\\" in raw:
        errors.append("local machine path leaked")
    if re.search(r"sk-proj-[A-Za-z0-9_-]{15,}|-----BEGIN (?:RSA |EC )?PRIVATE KEY-----", raw):
        errors.append("private secret pattern")
    return errors


def main() -> int:
    failed = False
    for page in PAGES:
        errors = check_page(ROOT / page)
        if errors:
            failed = True
            for err in errors:
                print(f"FAIL {page}: {err}")
        else:
            print(f"PASS {page}: HTML IDs, bilingual pairs, local links, secret hygiene")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
