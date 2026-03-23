#!/usr/bin/env python3
"""Convert SSOT discovery Markdown (pipe tables) to Notion-flavored Markdown with <table> blocks."""
from __future__ import annotations

import re
import sys
from pathlib import Path


def escape_cell(s: str) -> str:
    """Escape characters Notion treats specially inside table cells."""
    # Links [text](url) — keep; escape bare [ for tags like [ARCH]
    out = []
    i = 0
    while i < len(s):
        if s[i] == "[" and i + 1 < len(s):
            # markdown link?
            close = s.find("]", i)
            if close != -1 and close + 1 < len(s) and s[close + 1] == "(":
                paren = s.find(")", close + 2)
                if paren != -1:
                    out.append(s[i : paren + 1])
                    i = paren + 1
                    continue
            out.append("\\[")
            i += 1
            continue
        if s[i] == "$" and (i == 0 or s[i - 1] != "\\"):
            out.append("\\$")
            i += 1
            continue
        if s[i] == "|" and (i == 0 or s[i - 1] != "\\"):
            out.append("\\|")
            i += 1
            continue
        out.append(s[i])
        i += 1
    return "".join(out)


def split_row(line: str) -> list[str]:
    line = line.strip()
    if not line.startswith("|"):
        return []
    line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    parts = [p.strip() for p in line.split("|")]
    return parts


def is_separator_row(line: str) -> bool:
    t = line.strip().strip("|").replace(" ", "")
    return bool(re.match(r"^:?-+:?(?:\|:?-+:?)*$", t))


def convert_tables(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("|") and i + 1 < len(lines) and is_separator_row(lines[i + 1]):
            header = split_row(line)
            i += 2  # skip separator
            rows: list[list[str]] = [header]
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            out.append(table_to_html(rows))
            continue
        out.append(line)
        i += 1
    return "\n".join(out)


def table_to_html(rows: list[list[str]]) -> str:
    if not rows:
        return ""
    ncol = max(len(r) for r in rows)
    parts = ['<table header-row="true" fit-page-width="true">']
    for ri, row in enumerate(rows):
        parts.append("<tr>")
        for c in range(ncol):
            cell = row[c] if c < len(row) else ""
            parts.append(f"<td>{escape_cell(cell)}</td>")
        parts.append("</tr>")
    parts.append("</table>")
    return "\n".join(parts)


def strip_title_line(text: str) -> str:
    """Remove leading # line (page title lives in Notion DB)."""
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        return "\n".join(lines[1:]).lstrip("\n")
    return text


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: md_to_notion.py <input.md> <output.notion.md>", file=sys.stderr)
        sys.exit(1)
    src = Path(sys.argv[1]).read_text(encoding="utf-8")
    body = strip_title_line(src)
    body = convert_tables(body)
    Path(sys.argv[2]).write_text(body, encoding="utf-8")
    print(f"Wrote {sys.argv[2]} ({len(body)} chars)")


if __name__ == "__main__":
    main()
