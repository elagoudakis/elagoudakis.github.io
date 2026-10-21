# DScape

Source of [dscape.gr](https://dscape.gr): Earth observation images and stories by Manos Lagoudakis.

Built with Jekyll and a small custom theme, deployed to GitHub Pages by `.github/workflows/pages-deploy.yml`
on every push to `main`.

## Guides

| Guide | Read it when you want to... |
| --- | --- |
| [`docs/PUBLISHING.md`](docs/PUBLISHING.md) | create a post from finished images with `tools/dscape_post.py`, or publish a draft |
| [`docs/CONTENT-MODEL.md`](docs/CONTENT-MODEL.md) | know what each post field does, or use a component (slider, time series, video, deep zoom) |
| [`docs/MAINTENANCE.md`](docs/MAINTENANCE.md) | change site settings, understand deploys, check the domain, statistics, local preview, or fix a problem |
| [`docs/templates/`](docs/templates/) | write a post by hand |

## In short

- Images go in `assets/img/<post-slug>/` (one full-size version; smaller copies are made at deploy time). Never link images from LinkedIn or other sites.
- Components are demoed at [dscape.gr/lab/](https://dscape.gr/lab/).
- Theme: `_layouts/`, `_includes/`, `assets/css/main.css`, `assets/js/`. Fonts and libraries are self-hosted (licences next to the files).
