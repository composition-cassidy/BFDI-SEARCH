"""
Fetch YouTube thumbnails for episodes using yt-dlp search and save a thumbnail map.

- Uses EPISODES from episodes.py
- For each title, runs yt-dlp with ytsearch1:<title> BFDI to grab the first result thumbnail
- Saves thumbnails under server/exports/thumbnails
- Writes an index JSON at server/exports/thumbnails/index.json with:
    { "episode_title": {"filename": "<file>", "video_url": "<url>", "id": "<video_id>"}, ... }

Prereqs: yt-dlp installed (pip install yt-dlp). Internet access required for fetching.
Usage:
  python fetch_thumbnails.py
"""

import json
import os
from pathlib import Path

from yt_dlp import YoutubeDL

from episodes import EPISODES

OUT_DIR = Path(__file__).resolve().parent / "exports" / "thumbnails"
INDEX_PATH = OUT_DIR / "index.json"


def sanitize(name: str) -> str:
    return "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in name).strip("_") or "untitled"


def fetch_thumbnail(title: str, season: int | None = None):
    query = f"ytsearch1:{title} BFDI"
    if season:
        query = f"ytsearch1:{title} BFDI Season {season}"

    safe = sanitize(title)
    outtmpl = str(OUT_DIR / f"{safe}.%(ext)s")

    ydl_opts = {
        "skip_download": True,
        "writethumbnail": True,
        "writeinfojson": False,
        "quiet": True,
        "outtmpl": outtmpl,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=True)

    # Resolve thumbnail file (yt-dlp saves alongside)
    # Find the first file matching the safe prefix
    for ext in ("jpg", "png", "webp", "jpeg"):
        candidate = OUT_DIR / f"{safe}.{ext}"
        if candidate.exists():
            return candidate.name, info.get("webpage_url"), info.get("id")
    return None, info.get("webpage_url"), info.get("id")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    thumb_index = {}

    for ep in EPISODES:
        title = ep.get("title")
        season = ep.get("season")
        try:
            filename, url, vid = fetch_thumbnail(title, season)
            if filename:
                thumb_index[title] = {
                    "filename": filename,
                    "video_url": url,
                    "id": vid,
                }
                print(f"OK thumbnail for {title} -> {filename}")
            else:
                print(f"NO THUMB for {title} (id={vid} url={url})")
        except Exception as e:
            print(f"FAIL {title}: {e}")

    with INDEX_PATH.open("w", encoding="utf-8") as f:
        json.dump(thumb_index, f, ensure_ascii=False, indent=2)
    print(f"Wrote index: {INDEX_PATH} ({len(thumb_index)} entries)")


if __name__ == "__main__":
    main()
