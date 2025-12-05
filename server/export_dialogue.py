"""
Export dialogue documents from MongoDB to local JSON files.

Usage examples:
  python export_dialogue.py                   # exports all docs to exports/dialogue_export.json
  python export_dialogue.py --out my_dump.json
  python export_dialogue.py --per-episode     # writes one JSON per episode into exports/episodes/

Requires MONGODB_URI in .env (same as scraper). DB: BFDISearch, collection: BFDI_Dialogue.
"""

import argparse
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi

DB_NAME = "BFDISearch"
COLLECTION_NAME = "BFDI_Dialogue"
DEFAULT_OUT = Path(__file__).resolve().parent / "exports" / "dialogue_export.json"
DEFAULT_EPISODE_DIR = Path(__file__).resolve().parent / "exports" / "episodes"


def get_client():
    load_dotenv()
    uri = os.getenv("MONGODB_URI")
    if not uri:
        raise RuntimeError("MONGODB_URI not set in environment/.env")
    return MongoClient(uri, server_api=ServerApi("1"))


def export_all(collection, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    docs = list(collection.find({}))
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=2, default=str)
    return len(docs)


def sanitize_filename(name: str) -> str:
    return "".join(c if c.isalnum() or c in ("-", "_", " ") else "_" for c in name).strip().replace(" ", "_")


def export_per_episode(collection, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    episodes = collection.distinct("episode")
    total = 0
    for ep in episodes:
        docs = list(collection.find({"episode": ep}))
        total += len(docs)
        safe = sanitize_filename(ep or "unknown") or "unknown"
        out_path = out_dir / f"{safe}.json"
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(docs, f, ensure_ascii=False, indent=2, default=str)
    return total, len(episodes)


def main():
    parser = argparse.ArgumentParser(description="Export BFDI dialogue from MongoDB")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="Path to combined JSON export")
    parser.add_argument("--per-episode", action="store_true", help="Also write one JSON file per episode")
    parser.add_argument("--episode-dir", type=Path, default=DEFAULT_EPISODE_DIR, help="Directory for per-episode exports")
    args = parser.parse_args()

    client = get_client()
    collection = client[DB_NAME][COLLECTION_NAME]

    count = export_all(collection, args.out)
    print(f"Exported {count} documents to {args.out}")

    if args.per_episode:
        total, ep_count = export_per_episode(collection, args.episode_dir)
        print(f"Exported {total} documents across {ep_count} episode files into {args.episode_dir}")


if __name__ == "__main__":
    main()
