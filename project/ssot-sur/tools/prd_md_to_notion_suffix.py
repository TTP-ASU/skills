#!/usr/bin/env python3
"""Convert SSOT PRD markdown (§7 tail) to Notion-flavored markdown for MCP sync."""
from __future__ import annotations

import re
import sys
from pathlib import Path

def escape_rich(text: str) -> str:
    """Minimal escapes for Notion: $ (currency) and | inside table cells."""
    return text.replace("\\", "\\\\").replace("|", "\\|").replace("$", "\\$")


def is_table_sep(line: str) -> bool:
    s = line.strip()
    if not s.startswith("|"):
        return False
    return bool(re.match(r"^\|[\s\-:|]+\|\s*$", s))


def parse_md_table(lines: list[str], start: int) -> tuple[str, int]:
    """Return (xml_table, next_index)."""
    rows: list[list[str]] = []
    i = start
    while i < len(lines):
        line = lines[i]
        if not line.strip().startswith("|"):
            break
        if is_table_sep(line):
            i += 1
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append(cells)
        i += 1
    if not rows:
        return "", start

    buf = ['<table fit-page-width="true" header-row="true">']
    for row in rows:
        buf.append("<tr>")
        for cell in row:
            buf.append(f"<td>{escape_rich(cell)}</td>")
        buf.append("</tr>")
    buf.append("</table>")
    return "\n".join(buf), i


def convert_block(lines: list[str], i: int) -> tuple[str, int]:
    line = lines[i]
    stripped = line.strip()

    if stripped == "---":
        return "---\n", i + 1

    if stripped.startswith("### "):
        return stripped + "\n", i + 1
    if stripped.startswith("## "):
        return stripped + "\n", i + 1

    if stripped.startswith("> "):
        block = []
        while i < len(lines) and lines[i].strip().startswith(">"):
            block.append(lines[i].strip()[2:].lstrip())
            i += 1
        inner = "\n".join(escape_rich(b) for b in block)
        return f"> {inner}\n", i

    if stripped.startswith("|"):
        return parse_md_table(lines, i)

    if stripped.startswith("- "):
        out = []
        while i < len(lines) and lines[i].strip().startswith("- "):
            out.append("- " + escape_rich(lines[i].strip()[2:]))
            i += 1
        return "\n".join(out) + "\n", i

    if stripped == "":
        return "\n", i + 1

    # paragraph (may be multi-line until blank)
    para = [line]
    i += 1
    while i < len(lines) and lines[i].strip() != "":
        if lines[i].strip().startswith(("#", ">", "|", "-", "---")):
            break
        para.append(lines[i])
        i += 1
    text = "\n".join(para).strip()
    if not text:
        return "", i
    return escape_rich(text) + "\n\n", i


def main() -> None:
    prd = Path(__file__).resolve().parents[1] / "01-discovery" / "PRD-Functional-Requirements-SSOT-SUR.md"
    raw = prd.read_text(encoding="utf-8")
    lines = raw.splitlines()
    # Content after placeholder: from first FR table (line 123 in 1-based = index 122) to EOF
    start = 122  # 0-based: row 123 is | # | Requirement |
    chunk = lines[start:]
    i = 0
    parts: list[str] = []
    while i < len(chunk):
        block, ni = convert_block(chunk, i)
        if block:
            parts.append(block)
        if ni <= i:
            i += 1
        else:
            i = ni

    sys.stdout.write("".join(parts))


if __name__ == "__main__":
    main()
