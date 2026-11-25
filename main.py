#!/usr/bin/env python3
"""One-Line Laugh-Off entry: write exactly one funny line.

The joke is a single cold-read one-liner with a twist in its tail: an
elevator asked for life advice answers with a promise ("things are
looking up") and then delivers the opposite ("let me down") in the same
breath. The program is deterministic: it writes the line, and only the
line, to the harness output directory as entry.txt, then verifies the
write byte-for-byte with SHA-256. No network, no clock, no randomness:
two runs write identical bytes.

Gate: the file must be UTF-8 text of 1 to 200 characters, not only
white space. This line is 98 characters.
"""

import hashlib
import os
import sys
from pathlib import Path

JOKE = "I asked my elevator for life advice \u2014 it said things are looking up, then immediately let me down."

MAX_CHARS = 200


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    if not (1 <= len(JOKE) <= MAX_CHARS):
        print(f"joke is {len(JOKE)} characters, must be 1-{MAX_CHARS}", file=sys.stderr)
        return 1
    if not JOKE.strip():
        print("joke is only white space", file=sys.stderr)
        return 1
    JOKE.encode("utf-8")  # raises if not valid UTF-8

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    data = JOKE.encode("utf-8")
    target.write_bytes(data)

    if sha256_of(target) != hashlib.sha256(data).hexdigest():
        print("verification failed: entry.txt does not match the joke", file=sys.stderr)
        return 1
    print(f"wrote {target} ({len(JOKE)} characters, sha256 {sha256_of(target)[:16]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
