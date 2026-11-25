"""Entrypoint: draw the 25 November 2026 front page and write it out.

The grader runs this file twice in a sandbox with no network, a
read-only repository and a writable output directory. It must write
one image to <output>/entry.png, and both runs must produce the
same bytes: nothing here reads the clock, the network or any random
source, and the PNG encoder compresses at a fixed level.

Locally, run with MAKEFUN_OUTPUT_DIR=out to write ./out/entry.png;
in the grader the output directory is /output.
"""

import os
import sys

# The grader runs `python3 -P -s /bot/main.py`: safe-path mode (-P) does
# NOT put the script's directory on sys.path, so plain sibling imports
# (`from png import ...`) fail with ModuleNotFoundError and exit 1.
# Resolve the entry's own directory from __file__ and put it first.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from png import encode_png
from poster import WIDTH, HEIGHT, render_poster

OUTPUT_NAME = "entry.png"


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    canvas = render_poster()
    data = encode_png(WIDTH, HEIGHT, canvas.to_bytes())
    path = os.path.join(out_dir, OUTPUT_NAME)
    with open(path, "wb") as fh:
        fh.write(data)
    print(f"wrote {path} ({len(data)} bytes, {WIDTH}x{HEIGHT})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
