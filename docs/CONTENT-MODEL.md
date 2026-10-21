# DScape content model

Every post uses the same front matter, so the homepage grid, filters and maps can be built from it.
Templates: `docs/templates/snapshot.md` and `docs/templates/story.md`. The export tool (`PUBLISHING.md`) fills all of this in for you.

| Field | Required | Meaning |
| --- | --- | --- |
| `description` | yes | One sentence used for the homepage hero, search results and link previews |
| `kind` | yes | `snapshot` (one image + short caption, about one place) or `story` (longer post, possibly several images and places). Shown as a badge on the homepage tiles, as the label above the post title, and in the archive |
| `categories` | yes | Primary mission or data source, one value (Sentinel-2, CAMS, ...) |
| `tags` | yes | Topics, places, secondary missions |
| `image` | yes* | `path`: grid thumbnail, social preview and (by default) the picture at the top of the post; use a JPG or PNG, about 1200 × 630 or larger. `alt`: what it shows. Optional: `hero` (a different, uncropped image for the top of the post; the export tool sets this for snapshots), `caption`, `full` (link for "View full resolution"). *Missing = placeholder tile and site default share image |
| `acquired` | EO posts | Acquisition date `"YYYY-MM-DD"` or range `"YYYY-MM-DD/YYYY-MM-DD"` (quoted) |
| `location` | EO posts | `{ name, lat, lon }`, approximate scene centre |
| `locator` | stories | `true` shows the locator globe on a story. Snapshots always show it (they need `location` with `lat`/`lon`); stories hide it by default, because they often cover several places |
| `credit` | EO posts | Data attribution, e.g. "Contains modified Copernicus Sentinel data (2026)" |
| `linkedin` | no | URL of the LinkedIn cross-post; shows the "Discuss on LinkedIn" button |
| `grid` | no | `false` keeps a post out of the homepage grid (it still appears in the archive) |
| `noindex` | no | `true` asks search engines not to list the page (used by the lab page) |

Images live in `assets/img/<post-slug>/`, never hot-linked from LinkedIn or other sites.

Snapshot posts show `image` as the large picture at the top, so the body only needs the caption text. Story posts can add more images in the body: an image followed by an `_italic line_` renders as image plus caption.

## Interactive components

Drop these into a post body. Live demos: [dscape.gr/lab/](https://dscape.gr/lab/).

- **Before/after compare**: `{% include compare.html before="/assets/img/slug/a.webp" after="/assets/img/slug/b.webp" before_label="17 Aug 2024" after_label="20 Aug 2024" alt="What both images show" caption="Credits: ..." %}`. Both images must cover the same area at the same size; `start=30` moves the starting handle position.
- **Time series**: `{% include timeseries.html frames="/assets/img/slug/2021.webp, /assets/img/slug/2022.webp" labels="2021, 2022" alt="What every frame shows" caption="Credits: ..." interval=1500 start=0 %}`. Play/pause plus one button per frame (a slider above 12 frames). `badge=false` hides the corner label when the frames already show their date. Arrow keys step through frames.
- **Deep zoom**: first cut the full-resolution image into tiles: `python tools/make_dzi.py big_image.png assets/zoom/slug` (needs Pillow). Then `{% include zoom.html dzi="/assets/zoom/slug/image.dzi" preview="/assets/img/slug/preview.webp" alt="What it shows" caption="Credits: ..." %}`. A 7000 px scene makes about 760 tiles (9 MB); readers only download what they view.
- **Looping animation (MP4)**: `{% include video.html src="/assets/img/slug/anim.mp4" poster="/assets/img/slug/poster.webp" label="What it shows" caption="Credits: ..." %}`. Muted, looping, autoplays unless the reader prefers reduced motion. Encode for the web first (H.264, about 1920 px wide), e.g. `ffmpeg -i in.mp4 -vf scale=1920:-2 -c:v libx264 -crf 27 -pix_fmt yuv420p -movflags +faststart -an out.mp4`.

## Drafts

Unfinished posts go in `_drafts/` (no date in the file name). They are not published. How to publish one: `PUBLISHING.md`. Local preview: `MAINTENANCE.md`.

## Image sizes (automatic)

You only commit one version of each image. During every deploy, GitHub runs `tools/make_variants.py`, which makes 480, 800, 1200 and 1600 px copies, and `_plugins/responsive_images.rb` adds them to every `<img>` so phones download small files. Nothing to do by hand; local previews simply use the full-size images.
