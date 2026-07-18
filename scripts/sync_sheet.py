#!/usr/bin/env python3
"""Sync Harvey's Vocabulary Book Google Sheet -> data.js/data.json.

Reads the Google Sheet (source of truth) as CSV via the public gviz endpoint,
regenerates data.js and data.json, and bumps the ?v= cache-busting versions
in index.html for both data files.

Usage:
    python3 scripts/sync_sheet.py
"""
from __future__ import annotations

import csv
import io
import json
import re
import sys
import urllib.request
from datetime import date
from pathlib import Path

SPREADSHEET_ID = "14SHVvp1axGL9hThYTKc2Q78sL5C0pCNIad-16ZZsth0"
WORKSHEET_GID = 0
CSV_URL = (
    f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export"
    f"?format=csv&gid={WORKSHEET_GID}"
)

# Sheet header -> data.js field
FIELD_MAP = {
    "序号": "id",
    "单词": "word",
    "词性": "pos",
    "中文释义": "meaning",
    "英文例句": "example",
    "例句翻译": "exampleZh",
    "用法备注": "note",
    "来源课本": "book",
    "添加日期": "date",
}
# Sheet columns we ignore in data.js (kept in Sheet for study tracking)
IGNORED = {"掌握状态", "复习次数"}

ROOT = Path(__file__).resolve().parent.parent
DATA_JS = ROOT / "data.js"
DATA_JSON = ROOT / "data.json"
INDEX_HTML = ROOT / "index.html"


def fetch_csv(url: str) -> str:
    print(f"[sync] fetching {url}")
    with urllib.request.urlopen(url, timeout=60) as resp:
        return resp.read().decode("utf-8")


def parse_rows(csv_text: str) -> list[dict]:
    reader = csv.DictReader(io.StringIO(csv_text))
    rows: list[dict] = []
    for raw in reader:
        item: dict = {}
        for sheet_col, key in FIELD_MAP.items():
            v = (raw.get(sheet_col) or "").strip()
            if key == "id":
                try:
                    item[key] = int(v) if v else None
                except ValueError:
                    item[key] = v  # keep as-is if not integer
            else:
                item[key] = v
        if item.get("id") is None and not item.get("word"):
            continue  # skip empty rows
        rows.append(item)
    return rows


def write_data_js(rows: list[dict], out: Path) -> None:
    header = (
        "// Auto-generated vocabulary data (bundled fallback). "
        "Source: Harvey's Vocabulary Book Google Sheet.\n"
    )
    payload = json.dumps(rows, ensure_ascii=False)
    generated = date.today().isoformat()
    body = (
        f"window.VOCAB_DATA = {payload};\n"
        f'window.VOCAB_GENERATED = "{generated}";\n'
    )
    out.write_text(header + body, encoding="utf-8")
    print(f"[sync] wrote {out.name} ({len(rows)} rows, {out.stat().st_size} bytes)")


def write_data_json(rows: list[dict], out: Path) -> None:
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[sync] wrote {out.name} ({len(rows)} rows, {out.stat().st_size} bytes)")


def bump_index_cache(html_path: Path, files: list[str]) -> None:
    """Bump ?v=N for the given asset filenames in index.html (only if present)."""
    text = html_path.read_text(encoding="utf-8")
    for fname in files:
        pattern = re.compile(
            rf'({re.escape(fname)}\?v=)(\d+)'
        )
        def repl(m: re.Match) -> str:
            new_v = int(m.group(2)) + 1
            print(f"[sync] bump {fname}: v{m.group(2)} -> v{new_v}")
            return f"{m.group(1)}{new_v}"
        text, n = pattern.subn(repl, text)
        if n == 0:
            print(f"[sync] {fname}: no ?v= tag (skipped)")
    html_path.write_text(text, encoding="utf-8")


def main() -> int:
    csv_text = fetch_csv(CSV_URL)
    rows = parse_rows(csv_text)
    if not rows:
        print("[sync] ERROR: no rows parsed from CSV", file=sys.stderr)
        return 1
    # Sort by id (Sheet may have gaps; keep numeric order).
    rows.sort(key=lambda r: (r.get("id") is None, r.get("id") or 0))
    print(f"[sync] parsed {len(rows)} rows; last id = {rows[-1].get('id')}")

    write_data_js(rows, DATA_JS)
    write_data_json(rows, DATA_JSON)
    bump_index_cache(INDEX_HTML, ["data.js", "data.json"])
    print("[sync] done. Review with `git diff` before committing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
