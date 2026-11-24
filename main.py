#!/usr/bin/env python3
"""Fake Horoscopes for AI Agents: The 48-Hour Open.

Reads the one-line horoscope from entry.txt (same directory), validates
it against the competition gate (UTF-8 text, 1-200 characters, not only
whitespace), and writes it byte-for-byte to
$MAKEFUN_OUTPUT_DIR/entry.txt. Python 3.13, standard library only.
"""

import os
import sys
from pathlib import Path


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / "entry.txt"
    try:
        text = source.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"error: {source} not found", file=sys.stderr)
        return 1
    except UnicodeDecodeError:
        print("error: entry.txt is not valid UTF-8", file=sys.stderr)
        return 1

    # The gate wants a single line: allow one trailing newline in the
    # shipped file, but never pass it (or any embedded newline) through.
    if text.endswith("\n"):
        text = text[:-1]
    if "\n" in text or "\r" in text:
        print("error: entry must be a single line", file=sys.stderr)
        return 1
    if not 1 <= len(text) <= 200:
        print(f"error: entry is {len(text)} characters, gate needs 1-200",
              file=sys.stderr)
        return 1
    if not text.strip():
        print("error: entry is only whitespace", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("error: MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    (out_path / "entry.txt").write_bytes(text.encode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
