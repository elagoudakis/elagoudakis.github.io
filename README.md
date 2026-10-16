# DScape

Source of [dscape.gr](https://dscape.gr): Earth observation images and stories by Manos Lagoudakis.

Built with Jekyll and a small custom theme, deployed to GitHub Pages by `.github/workflows/pages-deploy.yml` on every push to `main`.

- New post: copy `docs/templates/snapshot.md` or `docs/templates/story.md` into `_posts/` (fields explained in `docs/CONTENT-MODEL.md`).
- Images: `assets/img/<post-slug>/`. Never link images from LinkedIn or other sites.
- Theme: `_layouts/`, `_includes/`, `assets/css/main.css`, `assets/js/site.js`. Fonts are self-hosted in `assets/fonts/` (SIL Open Font License).
