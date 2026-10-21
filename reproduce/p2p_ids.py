#!/usr/bin/env python3
"""Compare two *pre-extracted* Message-ID inventories (HTML pages vs mbox messages).

No network access. No mail bodies read. An input CSV has one row per page/message
and a header named message_id. This script does NOT itself parse Pipermail HTML or
mailbox files, and its output does not verify the archived 2026 counts without
the exact historical inputs and extraction conventions.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


def read_ids(path: Path) -> list[str | None]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames or "message_id" not in reader.fieldnames:
            raise ValueError(f"{path}: CSV must have a message_id column")
        ids: list[str | None] = []
        for row in reader:
            raw = (row.get("message_id") or "").strip()
            # Strip outer angle brackets only. Do not case-fold or alter internal
            # whitespace unless the historical normalization is documented.
            if raw.startswith("<") and raw.endswith(">"):
                raw = raw[1:-1]
            ids.append(raw or None)
        return ids


def compare(html_ids: list[str | None], mbox_ids: list[str | None]) -> dict:
    html = Counter(v for v in html_ids if v)
    mbox = Counter(v for v in mbox_ids if v)
    html_set, mbox_set = set(html), set(mbox)
    return {
        "html_page_rows": len(html_ids),
        "mbox_message_rows": len(mbox_ids),
        "html_rows_without_id": sum(v is None for v in html_ids),
        "mbox_rows_without_id": sum(v is None for v in mbox_ids),
        "matching_html_page_rows": sum(count for mid, count in html.items() if mid in mbox_set),
        "unmatched_html_page_rows_with_id": sum(count for mid, count in html.items() if mid not in mbox_set),
        "unmatched_mbox_unique_ids": len(mbox_set - html_set),
        "html_duplicate_id_groups": sum(count > 1 for count in html.values()),
        "mbox_duplicate_id_groups": sum(count > 1 for count in mbox.values()),
        "html_distinct_ids": len(html_set),
        "mbox_distinct_ids": len(mbox_set),
        "method": "per-row HTML page counting; unique mbox unmatched IDs; no case fold",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--html-index", type=Path, required=True)
    parser.add_argument("--mbox-index", type=Path, required=True)
    parser.add_argument("--output", type=Path, help="optional JSON output file")
    args = parser.parse_args()
    result = compare(read_ids(args.html_index), read_ids(args.mbox_index))
    value = json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True)
    if args.output:
        args.output.write_text(value + "\n", encoding="utf-8")
    print(value)


if __name__ == "__main__":
    main()
