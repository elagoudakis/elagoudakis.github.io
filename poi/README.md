# POI Capture

Offline-capable web app for capturing points of interest (GPS + name + group + note + photo).
All data stays in the phone's browser storage. Nothing is sent to any server.

## Install on DScape (GitHub Pages)
1. Copy this folder into the root of the `elagoudakis.github.io` repo, e.g. as `poi/`
   (any folder name works; all paths are relative).
2. Commit and push. After ~1 minute it is live at https://dscape.gr/poi/
3. Do not link to it from the site. The page has a `noindex` tag, so search engines skip it.
4. If the site is built with Jekyll and the jekyll-sitemap plugin, add to `_config.yml`:
       defaults:
         - scope: { path: "poi" }
           values: { sitemap: false }

## Install on the phone
Open https://dscape.gr/poi/ in Chrome, allow location, then menu (three dots) > "Add to Home screen" / "Install app".

## Updating the app
After changing any file, bump `VERSION` in `sw.js` (e.g. poi-v2) so phones pick up the new copy.
