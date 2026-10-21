#!/usr/bin/env python3
"""Turn finished visuals into a ready-to-commit DScape post.

Writes web-sized images, a share-safe JPG banner, optional deep-zoom tiles and
video, and a Markdown post with complete front matter, all inside the repo.

Command line (run from the repo root, or pass --repo):

  # One image, snapshot post
  python tools/dscape_post.py "Smoke over Ontario" --mission Sentinel-3 \
      --image final/smoke_20260712.png --acquired 2026-07-12 \
      --location "Ontario, Canada" --geotiff data/smoke_20260712.tif \
      --tags smoke,wildfire,canada --description "Smoke from ... on 12 July 2026."

  # Before/after slider
  python tools/dscape_post.py "Madeira fire" --mission Sentinel-2 \
      --compare before.jpg after.jpg --labels "17 Aug 2024,20 Aug 2024"

  # Time series (frames in order) and deep zoom
  python tools/dscape_post.py "CO in July" --mission Sentinel-5P \
      --frames co_2021.png co_2022.png co_2023.png --labels "2021,2022,2023"
  python tools/dscape_post.py "Taal" --mission Sentinel-2 --image s2.png --zoom

  Add --draft to write into _drafts/ (not published) instead of _posts/.

From Python (e.g. at the end of your pipeline):

  import sys; sys.path.append(r"C:\\path\\to\\elagoudakis.github.io\\tools")
  from dscape_post import make_post
  make_post("Smoke over Ontario", mission="Sentinel-3", image="final/smoke.png",
            acquired="2026-07-12", location="Ontario, Canada", geotiff="data/smoke.tif",
            repo=r"C:\\path\\to\\elagoudakis.github.io", draft=True)

Requires Pillow. Optional: rasterio (scene centre from --geotiff), ffmpeg on PATH (--video).
Inputs should be final 8-bit images (PNG/JPG/TIFF), e.g. your Photoshop exports.
Colour profiles such as Adobe RGB are converted to sRGB for the web.
"""
import argparse
import datetime as dt
import io
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata

from PIL import Image, ImageCms

Image.MAX_IMAGE_PIXELS = None

WEB_MAX = 2400            # longest side of in-post images (px)
WEB_QUALITY = 82
BANNER_SIZE = (2400, 1260)  # ~1.9:1, the link-preview shape
BANNER_QUALITY = 85


# --------------------------------------------------------------------------- helpers

def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return text or "post"


def q(value):
    """Quote a string for YAML (JSON strings are valid YAML)."""
    return json.dumps(value, ensure_ascii=False)


def default_credit(mission, year):
    m = (mission or "").lower()
    if m.startswith("sentinel") or m.startswith("copernicus"):
        return f"Contains modified Copernicus Sentinel data ({year})"
    if m.startswith("cams"):
        return f"Generated using Copernicus Atmosphere Monitoring Service information ({year})"
    if m.startswith("landsat"):
        return "USGS"
    return ""


def to_srgb(img):
    """Convert embedded colour profiles (e.g. Adobe RGB) to sRGB, and flatten to RGB."""
    icc = img.info.get("icc_profile")
    if icc:
        try:
            src = ImageCms.ImageCmsProfile(io.BytesIO(icc))
            if "srgb" not in ImageCms.getProfileName(src).lower():
                if img.mode not in ("RGB", "RGBA"):
                    img = img.convert("RGBA" if "A" in img.getbands() else "RGB")
                img = ImageCms.profileToProfile(img, src, ImageCms.createProfile("sRGB"),
                                                outputMode=img.mode)
        except Exception as exc:  # unusual profile: keep pixels as they are
            print(f"  note: colour profile not converted ({exc})")
    if img.mode in ("RGBA", "LA", "P"):
        rgba = img.convert("RGBA")
        bg = Image.new("RGB", rgba.size, (255, 255, 255))
        bg.paste(rgba, mask=rgba.split()[-1])
        return bg
    if img.mode in ("I;16", "I;16B", "I"):
        raise SystemExit("16-bit single-band input: export an 8-bit RGB image first.")
    return img.convert("RGB")


def open_image(path):
    if not os.path.isfile(path):
        raise SystemExit(f"Image not found: {path}")
    return to_srgb(Image.open(path))


def save_web(img, dst, size=None):
    if size:
        img = img.resize(size, Image.LANCZOS)
    elif max(img.size) > WEB_MAX:
        s = WEB_MAX / max(img.size)
        img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    img.save(dst, "WEBP", quality=WEB_QUALITY, method=6)
    return img.size


def save_banner(img, dst):
    """Centre-crop to the link-preview shape and save as JPG (LinkedIn may not show WebP)."""
    tw, th = BANNER_SIZE
    scale = max(tw / img.width, th / img.height)
    w, h = round(img.width * scale), round(img.height * scale)
    big = img.resize((w, h), Image.LANCZOS)
    left, top = (w - tw) // 2, (h - th) // 2
    big.crop((left, top, left + tw, top + th)).save(
        dst, "JPEG", quality=BANNER_QUALITY, optimize=True, progressive=True)


def geotiff_centre(path):
    """Scene centre (lat, lon) in degrees from a GeoTIFF, using rasterio if available."""
    try:
        import rasterio
        from rasterio.warp import transform
    except ImportError:
        print("  note: rasterio not installed, skipping --geotiff (pass --lat/--lon instead)")
        return None
    with rasterio.open(path) as ds:
        b = ds.bounds
        cx, cy = (b.left + b.right) / 2, (b.bottom + b.top) / 2
        if ds.crs and ds.crs.to_epsg() != 4326:
            xs, ys = transform(ds.crs, "EPSG:4326", [cx], [cy])
            cx, cy = xs[0], ys[0]
    return round(cy, 2), round(cx, 2)


def site_path(repo, path):
    return "/" + os.path.relpath(path, repo).replace(os.sep, "/")


# --------------------------------------------------------------------------- main API

def make_post(title, *, mission, image=None, compare=None, frames=None, video=None,
              labels=None, zoom=False, banner=None, kind=None, tags=None,
              description="", acquired=None, location=None, lat=None, lon=None,
              geotiff=None, credit=None, caption="", alt=None, linkedin=None, locator=False,
              date=None, slug=None, draft=False, repo=".", force=False):
    """Create the post and its assets. Returns the path of the Markdown file."""
    repo = os.path.abspath(repo)
    if not os.path.isfile(os.path.join(repo, "_config.yml")):
        raise SystemExit(f"Not a DScape repo (no _config.yml): {repo}")
    modes = [m for m in (image, compare, frames, video) if m]
    if len(modes) != 1:
        raise SystemExit("Give exactly one of: image, compare, frames, video.")

    date = date or dt.datetime.now().astimezone()
    if isinstance(date, str):
        date = dt.datetime.fromisoformat(date)
    year = acquired[:4] if acquired else date.strftime("%Y")
    slug = slug or slugify(title)
    kind = kind or ("story" if compare or frames else "snapshot")
    alt = alt or title
    tags = [t.strip() for t in (tags or []) if t.strip()]
    labels = [l.strip() for l in (labels or []) if l.strip()]
    credit = credit if credit is not None else default_credit(mission, year)

    img_dir = os.path.join(repo, "assets", "img", slug)
    folder = "_drafts" if draft else "_posts"
    md_name = f"{slug}.md" if draft else f"{date:%Y-%m-%d}-{slug}.md"
    md_path = os.path.join(repo, folder, md_name)
    if os.path.exists(md_path) and not force:
        raise SystemExit(f"Post already exists: {md_path} (use --force to overwrite)")

    if geotiff and (lat is None or lon is None):
        centre = geotiff_centre(geotiff)
        if centre:
            lat, lon = centre
    if kind == "snapshot" and (lat is None or lon is None):
        raise SystemExit("Snapshots always show the locator globe: give --lat/--lon or --geotiff "
                         "(or use --kind story).")
    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(os.path.dirname(md_path), exist_ok=True)

    print(f"Creating '{title}' -> {os.path.relpath(md_path, repo)}")
    body = []
    cap = caption or (f"Credits: {credit}" if credit else "")
    banner_src = None
    hero = None

    if image:
        src = open_image(image)
        name = f"{slug}.webp"
        size = save_web(src, os.path.join(img_dir, name))
        print(f"  image  {name} {size[0]}x{size[1]}")
        banner_src = src
        hero = site_path(repo, os.path.join(img_dir, name))  # full image at the top of the post
        if zoom:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import make_dzi
            out = os.path.join(repo, "assets", "zoom", slug)
            make_dzi.tile(src, out, "image")
            body.append("Zoom into the full-resolution image:")
            body.append(include("zoom", dzi=site_path(repo, os.path.join(out, "image.dzi")),
                                preview=site_path(repo, os.path.join(img_dir, name)),
                                alt=alt, caption=cap))

    elif compare:
        a, b = (open_image(p) for p in compare)
        if a.size != b.size:
            print(f"  note: resizing 'before' {a.size} to match 'after' {b.size}")
        names = [f"{slug}_before.webp", f"{slug}_after.webp"]
        size = save_web(b, os.path.join(img_dir, names[1]))
        save_web(a, os.path.join(img_dir, names[0]), size=size)
        print(f"  compare {names[0]} / {names[1]} {size[0]}x{size[1]}")
        bl = labels[0] if len(labels) > 0 else "Before"
        al = labels[1] if len(labels) > 1 else "After"
        body.append(include("compare", before=site_path(repo, os.path.join(img_dir, names[0])),
                            after=site_path(repo, os.path.join(img_dir, names[1])),
                            before_label=bl, after_label=al, alt=alt, caption=cap))
        banner_src = b

    elif frames:
        imgs = [open_image(p) for p in frames]
        size = None
        paths = []
        for i, im in enumerate(imgs):
            label = labels[i] if i < len(labels) else str(i + 1)
            name = f"{slug}_{slugify(label)}.webp"
            size = save_web(im, os.path.join(img_dir, name), size=size)
            paths.append(site_path(repo, os.path.join(img_dir, name)))
        if len(labels) < len(imgs):
            labels = labels + [str(i + 1) for i in range(len(labels), len(imgs))]
        print(f"  frames {len(imgs)} x {size[0]}x{size[1]}")
        body.append(include("timeseries", frames=", ".join(paths), labels=", ".join(labels),
                            alt=alt, caption=cap, start=len(imgs) - 1))
        banner_src = imgs[-1]

    elif video:
        if not shutil.which("ffmpeg"):
            raise SystemExit("ffmpeg not found on PATH (needed for --video).")
        mp4 = os.path.join(img_dir, f"{slug}.mp4")
        poster = os.path.join(img_dir, f"{slug}_poster.png")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-vf", "scale='min(1920,iw)':-2",
                        "-c:v", "libx264", "-preset", "slow", "-crf", "27", "-pix_fmt", "yuv420p",
                        "-movflags", "+faststart", "-an", mp4], check=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-sseof", "-0.5", "-i", video,
                        "-frames:v", "1", poster], check=True)
        banner_src = open_image(poster)
        poster_webp = poster.replace(".png", ".webp")
        save_web(banner_src, poster_webp)
        os.remove(poster)
        print(f"  video  {os.path.basename(mp4)} ({os.path.getsize(mp4) // 1024} KB)")
        body.append(include("video", src=site_path(repo, mp4), poster=site_path(repo, poster_webp),
                            label=alt, caption=cap))

    if banner:
        banner_src = open_image(banner)
    banner_name = f"{slug}_banner.jpg"
    save_banner(banner_src, os.path.join(img_dir, banner_name))
    print(f"  banner {banner_name} {BANNER_SIZE[0]}x{BANNER_SIZE[1]}")

    fm = ["---", f"title: {q(title)}"]
    fm.append(f"description: {q(description or '[One sentence for search results and link previews]')}")
    fm.append(f"date: {date:%Y-%m-%d %H:%M:%S %z}")
    fm.append(f"kind: {kind}")
    fm.append(f"categories: [{q(mission)}]")
    fm.append("tags: [" + ", ".join(q(t) for t in tags) + "]")
    fm += ["image:", f"  path: {site_path(repo, os.path.join(img_dir, banner_name))}", f"  alt: {q(alt)}"]
    if hero:
        fm.append(f"  hero: {hero}")
    if caption or (hero and cap):
        fm.append(f"  caption: {q(caption or cap)}")
    if acquired:
        fm.append(f"acquired: {q(acquired)}")
    if location or lat is not None:
        loc = [f"name: {q(location)}"] if location else []
        if lat is not None and lon is not None:
            loc += [f"lat: {lat}", f"lon: {lon}"]
        fm.append("location: { " + ", ".join(loc) + " }")
    if kind == "story" and locator and lat is not None:
        fm.append("locator: true")
    if credit:
        fm.append(f"credit: {q(credit)}")
    if linkedin:
        fm.append(f"linkedin: {linkedin}")
    fm.append("---")

    text = "\n".join(fm) + "\n\n"
    text += (description or "[Write one to three sentences: what, where, when, and what to look at.]") + "\n"
    if body:
        text += "\n" + "\n\n".join(body) + "\n"
    with open(md_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

    print("Done. Preview with:  bundle exec jekyll serve" + (" --drafts" if draft else ""))
    print("Publish with:        git add -A && git commit -m \"New post: " + title.replace('"', "'") + "\" && git push")
    return md_path


def include(name, **params):
    parts = [f'{k}={q(str(v))}' if not isinstance(v, int) else f"{k}={v}"
             for k, v in params.items() if v not in (None, "")]
    return "{% include " + name + ".html\n   " + "\n   ".join(parts) + " %}"


# --------------------------------------------------------------------------- CLI

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("title")
    ap.add_argument("--mission", required=True, help="primary mission, e.g. Sentinel-2, CAMS")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--image", help="one finished image")
    src.add_argument("--compare", nargs=2, metavar=("BEFORE", "AFTER"))
    src.add_argument("--frames", nargs="+", help="time-series frames, in order")
    src.add_argument("--video", help="animation (MP4/MOV/GIF), re-encoded for the web")
    ap.add_argument("--labels", default="", help="comma-separated labels for --compare/--frames")
    ap.add_argument("--zoom", action="store_true", help="with --image: add deep-zoom tiles")
    ap.add_argument("--banner", help="separate image for the banner (default: from the main image)")
    ap.add_argument("--kind", choices=["snapshot", "story"])
    ap.add_argument("--tags", default="")
    ap.add_argument("--description", default="")
    ap.add_argument("--acquired", help='"YYYY-MM-DD" or "YYYY-MM-DD/YYYY-MM-DD"')
    ap.add_argument("--location", help='place name, e.g. "Madeira, Portugal"')
    ap.add_argument("--lat", type=float)
    ap.add_argument("--lon", type=float)
    ap.add_argument("--geotiff", help="GeoTIFF to read the scene centre from (needs rasterio)")
    ap.add_argument("--locator", action="store_true",
                    help="stories: show the locator globe (snapshots always show it)")
    ap.add_argument("--credit", help="data credit (default depends on --mission)")
    ap.add_argument("--caption", default="")
    ap.add_argument("--alt", help="what the image shows (default: the title)")
    ap.add_argument("--linkedin", help="URL of the LinkedIn post")
    ap.add_argument("--date", help="post date, ISO format (default: now)")
    ap.add_argument("--slug", help="URL name (default: from the title)")
    ap.add_argument("--draft", action="store_true", help="write to _drafts/ (not published)")
    ap.add_argument("--repo", default=".", help="path to the site repo (default: current folder)")
    ap.add_argument("--force", action="store_true", help="overwrite an existing post")
    a = ap.parse_args(argv)
    make_post(a.title, mission=a.mission, image=a.image, compare=a.compare, frames=a.frames,
              video=a.video, labels=a.labels.split(","), zoom=a.zoom, banner=a.banner, kind=a.kind,
              tags=a.tags.split(","), description=a.description, acquired=a.acquired,
              location=a.location, lat=a.lat, lon=a.lon, geotiff=a.geotiff, credit=a.credit,
              caption=a.caption, alt=a.alt, linkedin=a.linkedin, locator=a.locator, date=a.date, slug=a.slug,
              draft=a.draft, repo=a.repo, force=a.force)


if __name__ == "__main__":
    main()
