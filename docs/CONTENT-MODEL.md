# DScape content model

Every post uses the same front matter, so the homepage grid, filters and maps can be built from it.
Templates: `docs/templates/snapshot.md` and `docs/templates/story.md`.

| Field | Required | Meaning |
| --- | --- | --- |
| `kind` | yes | `snapshot` (one image + short caption) or `story` (short blog post) |
| `categories` | yes | Primary mission or data source, one value (Sentinel-2, CAMS, ...) |
| `tags` | yes | Topics, places, secondary missions |
| `image` | yes* | Thumbnail for the grid and social preview (`path`, `alt`). *Missing = site default |
| `acquired` | EO posts | Acquisition date `"YYYY-MM-DD"` or range `"YYYY-MM-DD/YYYY-MM-DD"` (quoted) |
| `location` | EO posts | `{ name, lat, lon }`, approximate scene centre |
| `credit` | EO posts | Data attribution, e.g. "Contains modified Copernicus Sentinel data (2026)" |
| `linkedin` | no | URL of the LinkedIn cross-post |

Images live in `assets/img/<post-slug>/`, never hot-linked from LinkedIn or other sites.
