#!/usr/bin/env python3
"""news-image-20261120 entrypoint: copy the vendored infographic to /output.

Stdlib only, no network, deterministic: the output bytes are exactly the
bytes of entry.png shipped in this repository.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(SRC, "rb") as fh:
        blob = fh.read()
    if blob[:8] != b"\x89PNG\r\n\x1a\n":
        print("entry.png is not a PNG file", file=sys.stderr)
        return 1
    if len(blob) < 24 or blob[16:24] != (1024).to_bytes(4, "big") + (1024).to_bytes(4, "big"):
        print("entry.png is not 1024x1024", file=sys.stderr)
        return 1
    if len(blob) > 1048576:
        print("entry.png exceeds 1 MiB", file=sys.stderr)
        return 1
    with open(dst, "wb") as fh:
        fh.write(blob)
    with open(dst, "rb") as fh:
        written = fh.read()
    if written != blob:
        print("output differs from vendored entry.png", file=sys.stderr)
        return 1
    digest = hashlib.sha256(written).hexdigest()
    print(f"wrote {dst} ({len(written)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
