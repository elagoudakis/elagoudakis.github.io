# Publishing a post from the pipeline

`tools/dscape_post.py` turns finished visuals into a ready-to-commit post: web-sized WebP images,
a JPG banner for the grid and link previews, optional deep-zoom tiles or web video, and the
Markdown file with complete front matter.

## One-time setup (Windows / Miniconda)

```bash
conda install -c conda-forge pillow rasterio ffmpeg
```

Pillow is required. rasterio is only needed for `--geotiff` (scene centre for the locator globe),
ffmpeg only for `--video`.

## Typical use

Run from the repo folder. Add `--draft` while you write: the post goes to `_drafts/` and is not published.

| What you have | Command |
| --- | --- |
| One finished image | `python tools/dscape_post.py "Title" --mission Sentinel-3 --image final.png` |
| ...plus zoom into full resolution | add `--zoom` |
| Before/after pair | `--compare before.png after.png --labels "17 Aug,20 Aug"` |
| Frames over time | `--frames f2021.png f2022.png f2023.png --labels "2021,2022,2023"` |
| An animation | `--video animation.mp4` (also MOV or GIF) |

Snapshot or story: `--image` and `--video` make a snapshot, `--compare` and `--frames` make a story; `--kind snapshot|story` overrides this. Snapshots always show the locator globe, so they need `--geotiff` or `--lat/--lon`. For a story about one place, add `--locator` to show the globe too.

Useful extras: `--acquired 2026-07-12` (or a range `2026-07-10/2026-07-12`), `--location "Ontario, Canada"`,
`--geotiff scene.tif` (or `--lat 50.1 --lon -85.3`), `--tags smoke,wildfire`, `--description "..."`,
`--banner other.png` (different banner image), `--credit "..."` (default depends on the mission),
`--linkedin URL`.

## From your Python pipeline

```python
import sys
sys.path.append(r"C:\path\to\elagoudakis.github.io\tools")
from dscape_post import make_post

make_post(
    "Smoke over Ontario",
    mission="Sentinel-3",
    image=r"final\smoke_20260712.png",
    acquired="2026-07-12",
    location="Ontario, Canada",
    geotiff=r"data\smoke_20260712.tif",
    tags=["smoke", "wildfire", "canada"],
    repo=r"C:\path\to\elagoudakis.github.io",
    draft=True,
)
```

## Then

1. Open the new Markdown file and write the text (replace the [brackets]).
2. Check it: publish and look at the live site, or keep it as a draft and preview locally
   (setup in `MAINTENANCE.md`).
3. Commit and push. Without `--draft` the post goes live right away.

## Publishing a draft

1. Replace every [bracket] placeholder. To find any left: `findstr /n "[" _drafts\my-post.md`
   (lines with Markdown links and images contain brackets too; look for [DATE]-style placeholders).
2. If the front matter has a `date:` line, set it to today. Posts dated in the future are not shown.
3. Move it into `_posts/` with the date in front of the name (this also sets the address,
   `dscape.gr/posts/my-post/`):
   ```bash
   git mv _drafts/my-post.md _posts/2026-10-21-my-post.md
   ```
4. `git commit -m "Publish: My post"` and `git push`. Images stay where they are.

Images should be final 8-bit exports (for example from Photoshop). Adobe RGB and other colour
profiles are converted to sRGB automatically so colours look right in browsers.
