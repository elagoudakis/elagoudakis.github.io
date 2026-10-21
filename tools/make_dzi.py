#!/usr/bin/env python3
"""Cut a large image into Deep Zoom (DZI) tiles for DScape's zoom.html component.

Usage:
    python tools/make_dzi.py INPUT_IMAGE OUTPUT_DIR [--name NAME] [--quality 80]

Example:
    python tools/make_dzi.py Sentinel-2_postevent.png assets/zoom/taal-s2

Creates OUTPUT_DIR/NAME.dzi and OUTPUT_DIR/NAME_files/<level>/<col>_<row>.jpg
(NAME defaults to "image"). Needs only Pillow: pip install pillow
"""
import argparse
import math
import os

from PIL import Image

Image.MAX_IMAGE_PIXELS = None  # satellite scenes are big; trust the input

TILE = 254      # tile size without overlap (DZI convention)
OVERLAP = 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input")
    ap.add_argument("output_dir")
    ap.add_argument("--name", default="image")
    ap.add_argument("--quality", type=int, default=80)
    args = ap.parse_args()

    img = Image.open(args.input)
    if img.mode in ("RGBA", "LA", "P"):
        # Flatten transparency onto white so JPEG tiles look right.
        rgba = img.convert("RGBA")
        bg = Image.new("RGB", rgba.size, (255, 255, 255))
        bg.paste(rgba, mask=rgba.split()[-1])
        img = bg
    else:
        img = img.convert("RGB")

    w, h = img.size
    max_level = math.ceil(math.log2(max(w, h)))
    tiles_dir = os.path.join(args.output_dir, f"{args.name}_files")
    os.makedirs(tiles_dir, exist_ok=True)

    count = 0
    level_img = img
    for level in range(max_level, -1, -1):
        scale = 2 ** (max_level - level)
        lw, lh = max(1, math.ceil(w / scale)), max(1, math.ceil(h / scale))
        if level_img.size != (lw, lh):
            level_img = level_img.resize((lw, lh), Image.LANCZOS)
        ldir = os.path.join(tiles_dir, str(level))
        os.makedirs(ldir, exist_ok=True)
        for col in range(math.ceil(lw / TILE)):
            for row in range(math.ceil(lh / TILE)):
                x0 = max(0, col * TILE - OVERLAP)
                y0 = max(0, row * TILE - OVERLAP)
                x1 = min(lw, (col + 1) * TILE + OVERLAP)
                y1 = min(lh, (row + 1) * TILE + OVERLAP)
                level_img.crop((x0, y0, x1, y1)).save(
                    os.path.join(ldir, f"{col}_{row}.jpg"), "JPEG", quality=args.quality, optimize=True)
                count += 1

    with open(os.path.join(args.output_dir, f"{args.name}.dzi"), "w") as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<Image xmlns="http://schemas.microsoft.com/deepzoom/2008" Format="jpg" Overlap="{OVERLAP}" TileSize="{TILE}">\n'
            f'  <Size Width="{w}" Height="{h}"/>\n'
            '</Image>\n')
    print(f"{w}x{h} px, {max_level + 1} levels, {count} tiles -> {args.output_dir}")


if __name__ == "__main__":
    main()
