#!/usr/bin/env python3
"""Entry point for the make.fun news-image-20261119 v3 entry.

Copies the pre-built entry.png to $MAKEFUN_OUTPUT_DIR/entry.png.
Stdlib only, no network. Deterministic: byte-for-byte identical output
on every run (entry.png is built by build_image.py).
"""
import hashlib
import os
import shutil
import sys


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)
    digest = hashlib.sha256(open(dst, "rb").read()).hexdigest()
    print("wrote %s (%d bytes, sha256 %s)"
          % (dst, os.path.getsize(dst), digest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
