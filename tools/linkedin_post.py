#!/usr/bin/env python3
"""Bring one LinkedIn post into DScape as a draft snapshot or story.

Wraps dscape_post.py: it takes the LinkedIn URL and the post text and fills in
what dscape_post needs from them, then makes the post the usual way.

  - date:        decoded from the post URL (the original LinkedIn publication time)
  - linkedin:    the URL, cleaned of tracking parameters ("Discuss on LinkedIn" button)
  - body text:   the post text, cleaned (hashtags removed, emojis removed, paragraphs kept)
  - tags:        the post's hashtags (plus any --tags you add)
  - title:       --title, or the first line of the post if it is short
  - description: the first sentence of the post (override with --description)
  - credit:      taken from a "Credit:" / "Credits:" line in the post, if there is one

Usage (from the repo folder). Copy the post text from LinkedIn into a .txt file first:

  python tools/linkedin_post.py URL --text post.txt --mission Sentinel-2 \\
      --image original.png --lat 32.7 --lon -16.9 --acquired 2024-08-20

Every other dscape_post.py option works the same (--compare, --frames, --video,
--zoom, --kind, --location, --geotiff, --labels, ...). See docs/PUBLISHING.md.

  --paste          paste the text in the terminal instead of using --text
                   (end with Ctrl+Z then Enter on Windows, Ctrl+D on macOS/Linux)
  --fetch          experimental: read the text (and, with no image given, the picture)
                   from the public LinkedIn page. LinkedIn's picture is recompressed:
                   use your original whenever you have it.
  --dry-run        show what would be created (title, date, tags, text) and stop
  --publish        write straight to _posts/ instead of _drafts/

Requires Pillow (same setup as dscape_post.py).
"""
import argparse
import datetime as dt
import html
import json
import os
import re
import sys
import tempfile
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dscape_post  # noqa: E402

TITLE_MAX = 80
DESC_MAX = 200
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

# Lines LinkedIn readers know but a website reader doesn't need.
BOILERPLATE = re.compile(
    r"^\s*(\(?link (is )?in (the )?(first )?comments?\)?\.?|…\s*see more|\.\.\.see more|"
    r"see translation|follow me for more.*|repost.*if you.*|#?hashtags?:?)\s*$", re.I)
CREDIT_LINE = re.compile(r"^\s*(image\s+)?credits?\s*[:\-–]\s*(.+)$", re.I)
HASHTAG = re.compile(r"(?<![\w&])#([A-Za-z0-9_À-ɏͰ-Ͽ]+)")
EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF"
    "←-⇿⬀-⯿‍️⃣]+")
SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9“\"'(])")


# --------------------------------------------------------------------------- URL -> id, date

def post_id(url):
    """The numeric activity/share/ugcPost id in a LinkedIn post URL, or None."""
    m = re.search(r"(?:activity|share|ugcPost)[-:](\d{16,20})", url)
    if not m:
        m = re.search(r"\b(\d{19})\b", url)
    return int(m.group(1)) if m else None


def date_from_url(url):
    """LinkedIn ids carry their creation time: the first 41 bits are milliseconds since 1970."""
    pid = post_id(url)
    if not pid:
        return None
    when = dt.datetime.fromtimestamp((pid >> 22) / 1000, dt.timezone.utc)
    if not 2010 <= when.year <= dt.date.today().year + 1:
        return None
    return when.astimezone().replace(microsecond=0)  # your local time zone


def clean_url(url):
    """Drop ?utm_source=... and similar tracking from the URL."""
    parts = urllib.parse.urlsplit(url.strip())
    return urllib.parse.urlunsplit((parts.scheme or "https", parts.netloc, parts.path, "", ""))


# --------------------------------------------------------------------------- text

def clean_text(raw):
    """LinkedIn post text -> (markdown body, hashtags, credit or None)."""
    raw = raw.replace("\r\n", "\n").replace("\r", "\n")
    raw = re.sub(r"\bhashtag\s*#", "#", raw)  # copied hashtags sometimes read "hashtag#Sentinel2"
    tags, credit, lines = [], None, []
    for line in raw.split("\n"):
        tags += HASHTAG.findall(line)
        m = CREDIT_LINE.match(line)
        if m:
            credit = credit or m.group(2).strip().rstrip(".")
            continue
        stripped = HASHTAG.sub("", line).strip(" \t·|,")
        only_tags = line.strip() and not EMOJI.sub("", stripped).strip()
        if only_tags or BOILERPLATE.match(line):
            continue  # a line of hashtags only, or LinkedIn boilerplate
        line = HASHTAG.sub(r"\1", line)  # inline "#Sentinel2" -> "Sentinel2"
        line = EMOJI.sub("", line)
        line = re.sub(r"^\s*[•▪►–-]\s*", "- ", line)  # bullet-ish lines -> Markdown list items
        line = re.sub(r"[ \t]{2,}", " ", line).strip()
        lines.append(line)
    for i in range(len(lines) - 1, 0, -1):  # Markdown needs a blank line before a list
        if lines[i].startswith("- ") and lines[i - 1] and not lines[i - 1].startswith("- "):
            lines.insert(i, "")
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()
    text = re.sub(r"(?<![(<\]])(https?://\S+?)([.,)]?)(?=\s|$)", r"<\1>\2", text)  # bare URLs clickable
    seen, uniq = set(), []
    for t in tags:
        key = t.lower()
        if key not in seen:
            seen.add(key)
            uniq.append(key)
    return text, uniq, credit


def first_sentence(text, limit=DESC_MAX):
    para = next((p for p in text.split("\n\n") if p.strip() and not p.startswith("- ")), text)
    para = " ".join(para.split())
    s = SENTENCE_END.split(para, maxsplit=1)[0]
    if len(s) > limit:
        s = s[:limit].rsplit(" ", 1)[0].rstrip(",;:") + "…"
    return s


def guess_title(text):
    """The first line, if it reads like a headline; otherwise None."""
    first = text.split("\n", 1)[0].strip().strip("*_ ")
    if 0 < len(first) <= TITLE_MAX and not first.startswith("- "):
        return first.rstrip(".:")
    return None


def split_title(text):
    """If the first line is used as the title, drop it from the body."""
    title = guess_title(text)
    body = text.split("\n", 1)[1].strip() if title and "\n" in text else text
    return title, body or text


# --------------------------------------------------------------------------- optional fetch

def fetch_public(url):
    """Best effort: text and image URL of a public post. Returns (text or None, image or None)."""
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            page = r.read().decode("utf-8", "replace")
    except Exception as e:  # network, 999 "request denied", login wall...
        print(f"  fetch: could not read the LinkedIn page ({e})")
        return None, None
    text = image = None
    for block in re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', page, re.S):
        try:
            data = json.loads(block)
        except ValueError:
            continue
        for item in data if isinstance(data, list) else data.get("@graph", [data]):
            if not isinstance(item, dict):
                continue
            text = text or item.get("articleBody") or item.get("text")
            img = item.get("image")
            if isinstance(img, list):
                img = img[0] if img else None
            if isinstance(img, dict):
                img = img.get("url")
            image = image or img
    if not text:
        m = re.search(r'class="[^"]*attributed-text-segment-list__content[^"]*"[^>]*>(.*?)</p>', page, re.S)
        if m:
            text = re.sub(r"<br\s*/?>", "\n", m.group(1))
            text = re.sub(r"<[^>]+>", "", text)
    if not text:
        m = re.search(r'<meta[^>]+(?:property|name)="og:description"[^>]+content="([^"]*)"', page)
        if m:
            text = m.group(1)
            print("  fetch: only the short preview text was available; check the body is complete")
    if not image:
        m = re.search(r'<meta[^>]+property="og:image"[^>]+content="([^"]*)"', page)
        image = m.group(1) if m else None
    return (html.unescape(text).strip() if text else None), (html.unescape(image) if image else None)


def download(url, folder):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    path = os.path.join(folder, "linkedin_image.jpg")
    with open(path, "wb") as f:
        f.write(data)
    return path


# --------------------------------------------------------------------------- main

def has_source(rest):
    return any(a in rest for a in ("--image", "--compare", "--frames", "--video"))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
                                 usage="%(prog)s URL (--text FILE | --paste | --fetch) --mission M "
                                       "[--image ... | --compare ... | ...] [dscape_post options]")
    ap.add_argument("url", help="LinkedIn post URL (copy it from the post's ... menu > Copy link to post)")
    ap.add_argument("--text", help="text file with the post text, copied from LinkedIn")
    ap.add_argument("--paste", action="store_true", help="paste the post text into the terminal")
    ap.add_argument("--fetch", action="store_true", help="experimental: read text/picture from the public page")
    ap.add_argument("--title", help="post title (default: first line of the post, if short)")
    ap.add_argument("--description", help="one sentence (default: first sentence of the post)")
    ap.add_argument("--tags", default="", help="extra comma-separated tags, added to the hashtags")
    ap.add_argument("--no-hashtags", action="store_true", help="don't turn hashtags into tags")
    ap.add_argument("--credit", help="data credit (default: the post's Credit line, else by mission)")
    ap.add_argument("--date", help="override the date decoded from the URL (ISO format)")
    ap.add_argument("--publish", action="store_true", help="write to _posts/ (default: _drafts/)")
    ap.add_argument("--dry-run", action="store_true", help="show the result without writing files")
    a, rest = ap.parse_known_args(argv)

    url = clean_url(a.url)
    when = dt.datetime.fromisoformat(a.date) if a.date else date_from_url(url)
    if not when:
        raise SystemExit("Could not read the date from that URL: pass --date YYYY-MM-DDTHH:MM.")

    raw, fetched_image = None, None
    if a.text:
        with open(a.text, encoding="utf-8-sig") as f:
            raw = f.read()
    elif a.paste:
        print("Paste the post text, then Ctrl+Z and Enter (Windows) or Ctrl+D (macOS/Linux):")
        raw = sys.stdin.read()
    if a.fetch:
        print(f"Fetching {url}")
        text, fetched_image = fetch_public(url)
        raw = raw or text
    if not raw or not raw.strip():
        raise SystemExit("No post text: use --text post.txt, --paste or --fetch.")

    body, hashtags, credit_line = clean_text(raw)
    title_guess, body_wo_title = split_title(body)
    title = a.title or title_guess
    if a.title is None and title_guess:
        body = body_wo_title  # first line became the title
    if not title:
        raise SystemExit("The post has no short first line to use as a title: pass --title \"...\".")
    description = a.description or first_sentence(body)
    tags = ([] if a.no_hashtags else hashtags) + [t.strip().lower() for t in a.tags.split(",") if t.strip()]
    tags = list(dict.fromkeys(tags))

    extra = []
    if not has_source(rest):
        if fetched_image and not a.dry_run:
            folder = tempfile.mkdtemp(prefix="dscape_li_")
            extra = ["--image", download(fetched_image, folder)]
            print("  note: using LinkedIn's recompressed picture; replace it with your original if you can")
        elif not a.dry_run:
            raise SystemExit("Give the picture: --image original.png (or --compare / --frames / --video).")

    print(f"\nTitle:       {title}\nDate:        {when:%Y-%m-%d %H:%M %z}  (from the LinkedIn URL)"
          f"\nDescription: {description}\nTags:        {', '.join(tags) or '-'}"
          f"\nCredit:      {a.credit or credit_line or '(default for the mission)'}\nLinkedIn:    {url}"
          f"\n\n--- body ---\n{body}\n------------\n")
    if a.dry_run:
        print("Dry run: nothing written.")
        return None

    argv2 = [title] + rest + extra
    d = dscape_post.build_parser().parse_args(argv2)
    kw = dscape_post.args_to_kwargs(d)
    kw.update(date=when, linkedin=url, description=description, tags=tags,
              credit=a.credit or credit_line or d.credit, draft=not a.publish, text=body)
    return dscape_post.make_post(title, **kw)


if __name__ == "__main__":
    main()
