# BFDI Search

Search across Battle for Dream Island episode transcripts with filters by keywords, character, and season. Results link to transcript pages and show thumbnails served from local exports.

## Features
- Keyword/phrase search with character and season filters
- Episode info and transcript link per result
- Local JSON data source (no live DB) and optional YouTube thumbnails (yt-dlp)

## Requirements
- Node.js 18+
- Python 3 (for exporters/thumbnails)
- npm/yarn
- Optional: MongoDB URI in `.env` (only needed to re-export data)

## Setup
1) Install deps (run once):
   - `cd server && npm install`
   - `cd ../client && npm install`
2) Ensure `server/exports/dialogue_export.json` exists (run `python server/export_dialogue.py` if you have MongoDB data).
3) (Optional) Generate thumbnails: `cd server && pip install yt-dlp && python fetch_thumbnails.py`

## Run (two terminals)
- Terminal 1: `cd server` then `node index.js`
- Terminal 2: `cd server` then `npm run dev` (proxies frontend to backend)

Frontend served via Vite dev server (port 5173 by default), backend on port 5000.

## Environment
Create `server/.env` if exporting from MongoDB:
```
MONGODB_URI=mongodb+srv://...
```

## Data export (optional)
- Export MongoDB to JSON: `cd server && python export_dialogue.py --per-episode`
- Thumbnails: `python fetch_thumbnails.py` (writes to `server/exports/thumbnails/` and `index.json`).

## Attribution
Project inspired by SpongeSearch by CurtisTRY; adapted for BFDI transcripts.
