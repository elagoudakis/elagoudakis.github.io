#!/usr/bin/env python3
"""Make smaller copies of every image in assets/img for responsive loading.

For each image wider than 480 px it writes <name>-480, -800, -1200 and -1600.webp
(only sizes smaller than the original) into _variants/ (mirroring assets/img), and records
sizes in _data/image_variants.json. The plugin _plugins/responsive_images.rb then adds
srcset/width/height to every <img> that has variants.

GitHub Actions runs this before each build, so nothing needs to be committed.
Run it locally only if you want responsive images in a local preview:
    python tools/make_variants.py
"""
import json
import os
import re
import sys

from PIL import Image

Image.MAX_IMAGE_PIXELS = None
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "assets", "img")
OUT = os.path.join(ROOT, "_variants")          # copied into the site as /assets/img-v/
WIDTHS = (480, 800, 1200, 1600)
EXTS = (".jpg", ".jpeg", ".png", ".webp")


def main():
    manifest = {}
    made = 0
    for dirpath, dirs, files in os.walk(SRC):
        dirs[:] = [d for d in dirs if d not in ("favicons",)]
        for fn in sorted(files):
            if not fn.lower().endswith(EXTS) or re.search(r"-\d+\.webp$", fn):
                continue
            src = os.path.join(dirpath, fn)
            rel = os.path.relpath(src, ROOT).replace(os.sep, "/")
            try:
                with Image.open(src) as im:
                    w, h = im.size
                    entry = {"w": w, "h": h, "v": []}
                    stem = os.path.splitext(os.path.relpath(src, SRC))[0]
                    for tw in WIDTHS:
                        if tw >= w:
                            break
                        dst = os.path.join(OUT, f"{stem}-{tw}.webp")
                        if not (os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src)):
                            os.makedirs(os.path.dirname(dst), exist_ok=True)
                            th = round(h * tw / w)
                            frame = im.convert("RGB") if im.mode not in ("RGB",) else im
                            frame.resize((tw, th), Image.LANCZOS).save(dst, "WEBP", quality=72, method=4)
                            made += 1
                        entry["v"].append(tw)
                    manifest["/" + rel] = entry
            except Exception as exc:
                print(f"skip {rel}: {exc}", file=sys.stderr)
    os.makedirs(os.path.join(ROOT, "_data"), exist_ok=True)
    with open(os.path.join(ROOT, "_data", "image_variants.json"), "w") as f:
        json.dump(manifest, f, indent=0, sort_keys=True)
    print(f"{len(manifest)} images, {made} new variants")


if __name__ == "__main__":
    main()
