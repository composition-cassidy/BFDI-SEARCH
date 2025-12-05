const express = require('express');
const fs = require('fs');
const path = require('path');

const router = express.Router();

// Load dialogue from local export
const EXPORT_PATH = path.join(__dirname, '..', 'exports', 'dialogue_export.json');
const THUMB_INDEX_PATH = path.join(__dirname, '..', 'exports', 'thumbnails', 'index.json');
const EXPORT_LIMIT = 150;

let dialogueCache = [];
let thumbIndex = {};

function loadDialogue() {
  try {
    const raw = fs.readFileSync(EXPORT_PATH, 'utf-8');
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) {
      throw new Error('Export file is not an array');
    }
    dialogueCache = parsed;
    console.log(`Loaded ${dialogueCache.length} dialogue lines from ${EXPORT_PATH}`);
  } catch (err) {
    console.error(`Failed to load dialogue export at ${EXPORT_PATH}:`, err.message);
    dialogueCache = [];
  }
}

function loadThumbIndex() {
  try {
    const raw = fs.readFileSync(THUMB_INDEX_PATH, 'utf-8');
    const parsed = JSON.parse(raw);
    if (parsed && typeof parsed === 'object') {
      thumbIndex = parsed;
      console.log(`Loaded thumbnail index (${Object.keys(thumbIndex).length}) from ${THUMB_INDEX_PATH}`);
    } else {
      throw new Error('Thumbnail index is not an object');
    }
  } catch (err) {
    console.error(`Failed to load thumbnail index at ${THUMB_INDEX_PATH}:`, err.message);
    thumbIndex = {};
  }
}

// initial load
loadDialogue();
loadThumbIndex();

// helper filter
function matches(doc, keywords, character, season) {
  if (season !== undefined) {
    if (String(doc.season) !== String(season)) return false;
  }
  if (character) {
    const hay = (doc.character || '').toLowerCase();
    if (!hay.includes(character.toLowerCase())) return false;
  }
  if (keywords) {
    const hay = (doc.dialogue || '').toLowerCase();
    if (!hay.includes(keywords.toLowerCase())) return false;
  }
  return true;
}

function withThumbnail(doc) {
  const t = thumbIndex[doc.episode_title];
  if (t && t.filename) {
    const thumbPath = path.join(__dirname, '..', 'exports', 'thumbnails', t.filename);
    if (fs.existsSync(thumbPath)) {
      return { ...doc, thumbnail: `/thumbnails/${t.filename}` };
    }
  }
  return { ...doc, thumbnail: `/thumbnails/placeholder.jpg` };
}

// All dialogue (limited)
router.get('/', (req, res) => {
  if (!dialogueCache.length) {
    return res.status(503).send('Dialogue export not loaded');
  }
  res.status(200).send(dialogueCache.slice(0, EXPORT_LIMIT).map(withThumbnail));
});

// Dialogue w/ search queries
router.get('/search', (req, res) => {
  const { keywords, character, season } = req.query;

  if (!dialogueCache.length) {
    return res.status(503).send('Dialogue export not loaded');
  }

  const filtered = dialogueCache.filter((d) =>
    matches(d, keywords, character, season ? parseInt(season) : undefined)
  ).map(withThumbnail);

  res.status(200).send(filtered.slice(0, EXPORT_LIMIT));
});

module.exports = router;
