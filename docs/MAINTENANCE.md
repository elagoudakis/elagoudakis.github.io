# Running the site

Everything about keeping dscape.gr working: settings, how a deploy works, the domain, statistics,
local preview and what to do when something breaks. For writing posts see `PUBLISHING.md`;
for post fields and components see `CONTENT-MODEL.md`.

## Site settings (`_config.yml`)

| Setting | What it controls |
| --- | --- |
| Footer text (disclaimer) | Edit `_includes/footer.html` directly |
| `title`, `tagline`, `description` | Site name, the line next to the logo, and the default text for search results and link previews |
| `url` | Must stay `https://dscape.gr`: it sets the canonical address search engines use |
| `author.name`, `author.email` | Name in the footer and feed; `email` is the public contact address on the About page, the footer Email link and the RSS feed. Change it in this one place |
| `linkedin`, `github_profile` | Header icons, footer links and the About page |
| `goatcounter` | GoatCounter site code (e.g. `"dscape"`); empty turns visitor statistics off |
| `image` | Default share image for pages without their own |
| `timezone` | Used for post dates |

After changing `_config.yml`, commit and push like any other change.

## What happens when you push

Every push to `main` runs `.github/workflows/pages-deploy.yml` (see the **Actions** tab on GitHub):

1. **Make responsive image copies**: `tools/make_variants.py` creates 480–1600 px copies of every image (not stored in the repo).
2. **Build site**: Jekyll builds the pages; `_plugins/responsive_images.rb` adds the image copies to every `<img>`.
3. **Test site**: html-proofer checks that every internal link and image exists. A missing file stops the deploy, so a broken page never goes live.
4. **Deploy** to GitHub Pages. The live site updates 1–2 minutes after the push.

A red cross in Actions means the old site stays live. Click the run, then the red step, and read the error (or paste it to Claude).

## Where things live

| Folder / file | Contents |
| --- | --- |
| `_posts/`, `_drafts/` | Published posts and unpublished drafts |
| `about.md`, `archives.md`, `404.html`, `lab/` | Pages; `lab/` is the component test page (not in menus or search engines) |
| `_layouts/`, `_includes/` | Page templates and components (`compare`, `timeseries`, `video`, `zoom`, `locator`, ...) |
| `assets/css/main.css`, `assets/js/` | Styles and scripts; third-party libraries are self-hosted in `assets/js/lib/` |
| `assets/img/<post-slug>/` | Post images (one full-size version each) |
| `assets/zoom/<slug>/` | Deep-zoom tiles |
| `assets/fonts/` | Self-hosted fonts (no requests to Google) |
| `_plugins/` | Responsive-image plugin |
| `tools/` | `dscape_post.py` (new posts), `make_dzi.py` (zoom tiles), `make_variants.py` (image copies). Not published |
| `docs/` | These guides and the post templates. Not published |

## Domain and DNS

The domain is managed at your registrar. Records that must stay in place:

| Type | Name | Value | Purpose |
| --- | --- | --- | --- |
| A | `@` | 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153 | GitHub Pages |
| CNAME | `www` | `elagoudakis.github.io` | GitHub Pages (if you use www) |
| TXT | (as given by GitHub) | | Verified domain on your GitHub account (prevents takeover) |
| TXT | `@` | `google-site-verification=...` | Google Search Console (once verified) |

Email records (MX, SPF TXT) for a future dscape address can be added alongside; they don't affect the site.
**DNSSEC** is managed by the registrar. Before ever moving DNS to another provider (e.g. Cloudflare), turn DNSSEC off and wait a day, or the site and email stop resolving for many visitors. Adding or editing records is safe.

In the repo's **Settings → Pages**, the custom domain is `dscape.gr` and **Enforce HTTPS** is ticked.

## Visitor statistics (GoatCounter)

Set `goatcounter: "yourcode"` in `_config.yml`. Statistics are at `https://yourcode.goatcounter.com`.
No cookies and no personal data are collected; the footer says so automatically. Counting only happens on
the live site. To exclude your own visits, add your IP under GoatCounter **Settings → Ignore IPs**.

## Google Search Console

Property type **Domain** `dscape.gr`, verified with a DNS TXT record. Sitemap: `https://dscape.gr/sitemap.xml`
(generated automatically). Check it now and then for indexing problems.

## Previewing locally (optional)

Without a local setup, publish a post and check it on the live site, or keep it as a draft until it's ready.
For a full local preview on Windows:

1. Install Ruby with **RubyInstaller** (version 3.3 *with Devkit*) from rubyinstaller.org; let it run `ridk install` at the end.
2. In the repo folder: `gem install bundler`, then `bundle install` (first time only).
3. Run `bundle exec jekyll serve --drafts` and open http://localhost:4000. Stop with Ctrl+C.

Local previews show full-size images and no statistics; both are normal.

## Applying a package from Claude

1. Unzip it **outside** the repo (e.g. in Downloads). Never unzip inside the repo: a stray `_posts` folder would publish duplicate posts.
2. If Claude lists files to delete, delete them first.
3. Copy the package contents into the repo, replacing files.
4. `git add -A`, `git commit -m "..."`, `git push`, then watch the Actions tab.

## Git quick reference

```bash
git pull                     # get the latest from GitHub first
git status                   # see what changed
git add -A                   # stage everything
git commit -m "Message"      # save a snapshot
git push                     # publish (starts a deploy)
git mv old/path new/path     # move or rename a file
```

## Troubleshooting

| Problem | Fix |
| --- | --- |
| `git push`: "Invalid username or token" | Remove the saved GitHub login: `(echo protocol=https& echo host=github.com) \| git credential reject`, then push again and sign in in the browser |
| `git push` rejected: "remote contains work" | `git pull --rebase`, then `git push` |
| `git push` refused because of the "workflow" scope | Changes to `.github/workflows/` need a login with workflow permission; sign in again via the browser prompt, or use a token with `repo` and `workflow` scopes |
| `git commit` opens Vim | Type a message, then `Esc`, `:wq`, Enter. To use Nano instead: `git config --global core.editor nano` |
| "Deletion of directory failed" (Windows) | A program or OneDrive has the folder open; close it or pause OneDrive, then answer `y`. Consider moving the repo out of OneDrive (e.g. `C:\dev\`) |
| A post doesn't appear | Its `date:` is in the future, it is still in `_drafts/`, or the build failed (check Actions) |
| A post appears twice | A copy of `_posts/` exists elsewhere in the repo (often an unzipped package); delete it |
| Old Chirpy page still shows | Reload with Ctrl+F5; the old offline cache retires itself on the first visit |
| Images look broken | Image paths are case-sensitive on the live site: `Madeira.jpg` and `madeira.jpg` are different files |
