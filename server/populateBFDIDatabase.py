# -*- coding: utf-8 -*-
"""
BFDI Search - Database Population Script v8 (SMART PARSER)

MAJOR IMPROVEMENTS:
- Parses <b> tags for character names (BFDI wiki standard)
- Expanded character list (80+ characters)
- Filters episode titles, section headers, creator commentary
- Stricter dialogue validation
- Better speaker tracking
"""

import cloudscraper
import os
import re
import time
import random
from datetime import datetime
from pathlib import Path
from urllib.parse import quote
from bs4 import BeautifulSoup, NavigableString
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from episodes import EPISODES

load_dotenv()

# =============================================================================
# CONFIGURATION
# =============================================================================

uri = os.getenv('MONGODB_URI')
client = MongoClient(uri, server_api=ServerApi('1'))

DB_NAME = "BFDISearch"
COLLECTION_NAME = "BFDI_Dialogue"

db = client[DB_NAME]
collection = db[COLLECTION_NAME]

WIKI_BASE = "https://battlefordreamisland.fandom.com/wiki"

BASE_DELAY = 4.0
MAX_RETRIES = 5

# Control behavior
CLEAR_EXISTING = False          # If True, wipe collection before scrape
SKIP_EPISODES_WITH_DATA = True  # If True, skip episodes already in DB

scraper = cloudscraper.create_scraper(
    browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
)

# =============================================================================
# LOGGING
# =============================================================================
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / f"scrape_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

HTML_DIR = Path(__file__).resolve().parent.parent / "html"


def log(message):
    msg = str(message)
    print(msg)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(msg + "\n")


# =============================================================================
# EXPANDED CHARACTER LIST (80+ characters)
# =============================================================================

KNOWN_CHARACTERS = {
    # Hosts
    'announcer', 'four', 'two', 'x', 'one', 'purple face',
    'firey speaker box', 'flower speaker box', 'puffball speaker box',
    
    # Original BFDI contestants
    'blocky', 'bubble', 'coiny', 'david', 'eraser', 'firey', 'flower',
    'golf ball', 'ice cube', 'leafy', 'match', 'needle', 'pen', 'pencil',
    'pin', 'rocky', 'snowball', 'spongy', 'teardrop', 'tennis ball', 'woody',
    
    # BFDIA additions
    'book', 'bomby', 'dora', 'fries', 'gelatin', 'golf ball', 'nickel',
    'puffball', 'ruby', 'yellow face',
    
    # BFB/TPOT additions  
    'balloony', 'barf bag', 'basketball', 'bell', 'black hole', 'bottle',
    'bracelety', 'cake', 'clock', 'cloudy', 'eggy', 'fanny', 'firey jr',
    'foldy', 'gaty', 'grassy', 'lightning', 'liy', 'lollipop', 'loser',
    'marker', 'naily', 'pie', 'pillow', 'price tag', 'profily', 'remote',
    'robot flower', 'roboty', 'saw', 'stapy', 'taco', 'tree', 'tv', 'winner',
    'donut',
    
    # Alternate names / nicknames
    'gb', 'tb', 'td', 'icy', 'needy', 'leafy', 'firey',
    '8-ball', 'eight ball',
    
    # Groups and other
    'everyone', 'all', 'both', 'contestants', 'freesmart', 'team',
    'narrator', 'announcer at stake', 'speaker', 'host',
    
    # Creators (filter these out but recognize them)
    'cary', 'michael', 'jacknjellify',
}

# Episode titles to filter out (these appear as garbage in transcripts)
EPISODE_TITLES = {ep['title'].lower() for ep in EPISODES}

# Section headers and garbage patterns to filter
GARBAGE_PATTERNS = [
    r'^contents$',
    r'^transcript$',
    r'^gallery$',
    r'^trivia$',
    r'^goofs$',
    r'^continuity$',
    r'^references$',
    r'^the beginning$',
    r'^intro$',
    r'^opening$',
    r'^ending$',
    r'^credits$',
    r'^cake at stake',
    r'^after the intro',
    r'^before cake at stake',
    r'^after cake at stake',
    r'^the contest',
    r'^elimination$',
    r'^stinger$',
    r'^cold open',
    r'^categories$',
    r'^\d+$',  # Just numbers
    r'^episode \d+',
    r'^\[\d+\]$',  # References like [1]
    r'^edit$',
    r'^edit source$',
    r'well rested$',  # Common garbage
    r'look who it is$',
]

# Creator commentary patterns to filter
CREATOR_PATTERNS = [
    r"^hi,? it'?s me,? cary",
    r"^hey,? it'?s cary",
    r"^this is cary",
    r"^thank you (so much )?for watching",
    r"^don'?t forget to (vote|subscribe|like)",
    r"^see you (next time|in the next)",
    r"^if you enjoyed",
    r"^make sure to",
    r"^leave a comment",
    r"^the voting",
]

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_existing_episodes():
    existing = collection.distinct('episode_title')
    return set(existing)


def build_transcript_url(title):
    url_title = title.replace(" ", "_")
    url_title = quote(url_title, safe="_:!'(),")
    return f"{WIKI_BASE}/{url_title}/Transcript"


def normalized_key(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())


def find_local_html(title):
    """
    Look for a saved HTML transcript in ../html matching the episode title.
    Returns Path or None.
    """
    if not HTML_DIR.exists():
        return None
    target_key = normalized_key(title)
    for html_file in HTML_DIR.glob("*.html"):
        name_key = normalized_key(html_file.name)
        if target_key in name_key:
            return html_file
    return None


def get_title_card_image(soup):
    try:
        img = soup.find('img', {'class': 'pi-image-thumbnail'})
        if img and img.get('src'):
            return img['src'].split("/revision")[0]
    except:
        pass
    return None


def normalize_character(name):
    """Normalize character name for matching."""
    name = name.lower().strip()
    name = re.sub(r'[^\w\s\-]', '', name)  # Remove punctuation except hyphen
    name = re.sub(r'\s+', ' ', name)  # Normalize whitespace
    
    # Common corrections
    corrections = {
        'ice-cube': 'ice cube',
        'icecube': 'ice cube',
        'golfball': 'golf ball',
        'tennisball': 'tennis ball',
        'yellowface': 'yellow face',
        'yellow-face': 'yellow face',
        'blackhole': 'black hole',
        'black-hole': 'black hole',
        'barfbag': 'barf bag',
        'barf-bag': 'barf bag',
        'fireysr': 'firey',
        'fireyjr': 'firey jr',
        'firey-jr': 'firey jr',
        'robotflower': 'robot flower',
        'robot-flower': 'robot flower',
        'pricetag': 'price tag',
        'price-tag': 'price tag',
    }
    
    return corrections.get(name, name)


def is_known_character(name):
    """Check if name is a known character."""
    normalized = normalize_character(name)
    return normalized in KNOWN_CHARACTERS


def is_garbage(text):
    """Check if text is garbage that should be filtered."""
    text_lower = text.lower().strip()
    
    # Too short
    if len(text_lower) < 3:
        return True
    
    # Is an episode title
    if text_lower in EPISODE_TITLES:
        return True
    
    # Matches garbage patterns
    for pattern in GARBAGE_PATTERNS:
        if re.search(pattern, text_lower):
            return True
    
    # Matches creator commentary
    for pattern in CREATOR_PATTERNS:
        if re.search(pattern, text_lower):
            return True
    
    # Ends with [] (wiki section header artifact)
    if text_lower.endswith('[]'):
        return True
    
    # Just a timestamp like "0:00" or "12:34"
    if re.match(r'^\d{1,2}:\d{2}$', text_lower):
        return True
    
    return False


def is_stage_direction(text):
    """Check if text is a stage direction."""
    text = text.strip()
    if not text:
        return True
    # Full brackets
    if (text.startswith('[') and text.endswith(']')) or \
       (text.startswith('(') and text.endswith(')')):
        return True
    return False


def extract_dialogue_from_table(table):
    """
    Handle transcripts that are laid out as small two-column tables:
    first cell has an image (character), second cell has the line.
    """
    # Try to find a character from any image alt/data attributes.
    character = None
    for img in table.find_all('img'):
        alt = (img.get('alt') or img.get('data-image-name') or "").strip()
        if not alt:
            continue
        norm = normalize_character(alt)
        if is_known_character(norm):
            character = norm
            break

    if not character:
        return None

    # Pick the text cell (non-image).
    text_candidates = []
    for td in table.find_all('td'):
        if td.find('img'):
            continue
        text = td.get_text(separator=' ', strip=True)
        if text:
            text_candidates.append(text)

    if not text_candidates:
        return None

    dialogue = max(text_candidates, key=len).strip()
    if not dialogue or is_stage_direction(dialogue) or is_garbage(dialogue):
        return None

    return {
        'character': character,
        'dialogue': dialogue
    }


def extract_dialogue_bruteforce_tables(soup):
    """
    Very permissive fallback for stubborn pages:
    - Any table with an <img> whose alt or data-image-name yields a character.
    - Picks the longest non-image cell text.
    """
    lines = []
    for table in soup.find_all('table'):
        character = None
        for img in table.find_all('img'):
            alt = (img.get('alt') or img.get('data-image-name') or "").strip()
            if not alt:
                continue
            norm = normalize_character(alt)
            if is_known_character(norm):
                character = norm
                break
        if not character:
            continue

        text_candidates = []
        for td in table.find_all('td'):
            if td.find('img'):
                continue
            text = td.get_text(separator=' ', strip=True)
            if text:
                text_candidates.append(text)
        if not text_candidates:
            continue
        dialogue = max(text_candidates, key=len).strip()
        if dialogue and not is_stage_direction(dialogue) and not is_garbage(dialogue):
            lines.append({'character': character, 'dialogue': dialogue})
    return lines


def extract_dialogue_from_paragraph(p_tag, episode_title):
    """
    Extract dialogue from a paragraph tag.
    BFDI wiki often formats as: <b>Character</b>: Dialogue text
    Or: <b>Character:</b> Dialogue text
    """
    results = []
    
    # Get the full text
    full_text = p_tag.get_text(separator=' ', strip=True)
    
    if not full_text or is_garbage(full_text) or is_stage_direction(full_text):
        return results
    
    # Strategy 1: Look for bold tags containing character names
    bold_tags = p_tag.find_all('b')
    
    for bold in bold_tags:
        bold_text = bold.get_text(strip=True)
        
        # Clean up the bold text (remove trailing colon)
        char_name = bold_text.rstrip(':').strip()
        
        if is_known_character(char_name):
            # Get the dialogue after this bold tag
            dialogue_parts = []
            
            for sibling in bold.next_siblings:
                if isinstance(sibling, NavigableString):
                    text = str(sibling).strip()
                    if text.startswith(':'):
                        text = text[1:].strip()
                    if text:
                        dialogue_parts.append(text)
                elif sibling.name == 'b':
                    # Next character's line, stop here
                    break
                elif sibling.name in ['i', 'em']:
                    # Italics might be stage direction, skip
                    continue
                else:
                    text = sibling.get_text(strip=True)
                    if text and not is_stage_direction(text):
                        dialogue_parts.append(text)
            
            dialogue = ' '.join(dialogue_parts).strip()
            dialogue = re.sub(r'^[:\s]+', '', dialogue)  # Remove leading colons/spaces
            
            if dialogue and len(dialogue) > 2 and not is_garbage(dialogue):
                results.append({
                    'character': normalize_character(char_name),
                    'dialogue': dialogue
                })
    
    # Strategy 2: If no bold tags found, try "Character: Dialogue" pattern
    if not results:
        # Pattern: "CharacterName: dialogue text"
        match = re.match(r'^([A-Za-z][A-Za-z\s\-\'\.]{1,25}):\s*(.+)$', full_text)
        if match:
            char_name = match.group(1).strip()
            dialogue = match.group(2).strip()
            
            if is_known_character(char_name) and dialogue and not is_garbage(dialogue):
                results.append({
                    'character': normalize_character(char_name),
                    'dialogue': dialogue
                })
    
    return results


def parse_dialogue_advanced(soup, episode_title):
    """
    Advanced parsing that handles multiple transcript formats.
    """
    dialogue_lines = []
    
    # Find the content div
    content_div = soup.find('div', {'class': 'mw-parser-output'})
    if not content_div:
        content_div = soup.find('div', {'id': 'mw-content-text'})
    if not content_div:
        # Fallback to article/body to avoid hard failure on render snapshots
        content_div = soup.find('article') or soup.find('body') or soup
    
    # Remove table of contents
    for toc in content_div.find_all('div', {'id': 'toc'}):
        toc.decompose()
    for toc in content_div.find_all('div', {'class': 'toc'}):
        toc.decompose()

    # Remove citation footnotes that pollute dialogue text
    for ref in content_div.find_all(['sup', 'span'], {'class': 'reference'}):
        ref.decompose()
    
    # Remove navboxes/infoboxes but keep small dialogue tables; leave wikitables for bruteforce fallback
    for table in content_div.find_all('table'):
        classes = table.get('class', [])
        if any(c in ['navbox', 'infobox', 'toccolours', 'mw-collapsible'] for c in classes):
            table.decompose()
    
    # Remove navigation elements
    for nav in content_div.find_all(['nav', 'aside', 'footer']):
        nav.decompose()
    
    # Remove category links
    for cat in content_div.find_all('div', {'class': 'categories'}):
        cat.decompose()
    
    # Process paragraphs
    for p in content_div.find_all('p'):
        lines = extract_dialogue_from_paragraph(p, episode_title)
        dialogue_lines.extend(lines)

    # Process dialogue-style tables (image + text layout)
    for table in content_div.find_all('table'):
        line = extract_dialogue_from_table(table)
        if line:
            dialogue_lines.append(line)

    # Bruteforce tables as a fallback (runs even if we already found some)
    brute_lines = extract_dialogue_bruteforce_tables(content_div)
    dialogue_lines.extend(brute_lines)

    # Also check for dialogue in list items (some transcripts use <li>)
    for li in content_div.find_all('li'):
        # Skip TOC items
        parent = li.find_parent('div', {'id': 'toc'})
        if parent:
            continue
        
        li_text = li.get_text(strip=True)
        
        # Try "Character: Dialogue" pattern
        match = re.match(r'^([A-Za-z][A-Za-z\s\-\'\.]{1,25}):\s*(.+)$', li_text)
        if match:
            char_name = match.group(1).strip()
            dialogue = match.group(2).strip()
            
            if is_known_character(char_name) and dialogue and not is_garbage(dialogue):
                dialogue_lines.append({
                    'character': normalize_character(char_name),
                    'dialogue': dialogue
                })
    
    # Deduplicate while preserving order
    seen = set()
    unique_lines = []
    for line in dialogue_lines:
        key = (line['character'], line['dialogue'][:50])  # Use first 50 chars for dedup
        if key not in seen:
            seen.add(key)
            unique_lines.append(line)
    
    return unique_lines, None


def fetch_page_with_retry(url, max_retries=MAX_RETRIES):
    def do_request(target_url, attempt, note=""):
        try:
            response = scraper.get(target_url, timeout=30)
            return response, None
        except Exception as e:
            return None, f"{note}request error: {e}"

    render_suffix = "?action=render"
    for attempt in range(max_retries):
        wait = 0
        if attempt > 0:
            wait = (attempt + 1) * 5 + random.uniform(1, 3)
            log(f"    Waiting {wait:.1f}s before retry...")
            time.sleep(wait)

        # Try normal page
        response, err = do_request(url, attempt)
        if err:
            if attempt >= max_retries - 1:
                return None, err, False
            continue

        status = response.status_code
        content_len = len(response.content)

        if status == 404:
            return None, "Page not found (404)", False

        if status in (429, 503):
            if attempt >= max_retries - 1:
                return None, f"HTTP {status}", False
            log(f"    HTTP {status}, will retry after backoff")
            continue

        if status != 200:
            if attempt >= max_retries - 1:
                return None, f"HTTP {status}", False
            log(f"    HTTP {status}, retrying...")
            continue

        if content_len < 4000:
            # Fallback to rendered view to strip junk and bypass short bodies
            render_url = url + render_suffix
            render_resp, render_err = do_request(render_url, attempt, note="render ")
            if render_err is None and render_resp.status_code == 200 and len(render_resp.content) >= 2000:
                log(f"    Used action=render fallback (len={len(render_resp.content)})")
                return render_resp, None, True

            if attempt >= max_retries - 1:
                return None, f"Response too small ({content_len} bytes)", False
            log(f"    Response too small ({content_len} bytes), retrying...")
            continue

        return response, None, False

    return None, "Max retries exceeded", False


def scrape_episode(episode):
    title = episode['title']
    number = episode['number']
    season = episode['season']
    season_name = episode.get('season_name', f'Season {season}')
    
    transcript_url = build_transcript_url(title)
    log(f"\n[{number}] Scraping: {title}")
    log(f"    URL: {transcript_url}")
    
    soup = None
    used_local = False
    local_path = find_local_html(title)
    if local_path:
        try:
            log(f"    Using local HTML: {local_path.name}")
            with local_path.open("r", encoding="utf-8", errors="ignore") as f:
                html = f.read()
            soup = BeautifulSoup(html, "html.parser")
            used_local = True
        except Exception as e:
            log(f"    Failed to read local HTML ({local_path.name}): {e}")
    
    # If no local soup, fetch from web
    if soup is None:
        response, error, _ = fetch_page_with_retry(transcript_url)
        if error:
            log(f"    SKIP: {error}")
            return 0
        soup = BeautifulSoup(response.content, "html.parser")
    
    try:
        image_url = get_title_card_image(soup)
        dialogue_lines, parse_error = parse_dialogue_advanced(soup, title)
        
        if parse_error:
            log(f"    {parse_error}")
        
        if not dialogue_lines:
            # If local HTML yielded nothing, try network fetch as fallback
            if used_local:
                log("    Local HTML produced no dialogue; attempting live fetch fallback...")
                response, error, _ = fetch_page_with_retry(transcript_url)
                if error:
                    log(f"    Fallback fetch failed: {error}")
                    return 0
                soup = BeautifulSoup(response.content, "html.parser")
                image_url = get_title_card_image(soup)
                dialogue_lines, parse_error = parse_dialogue_advanced(soup, title)
                if parse_error:
                    log(f"    {parse_error}")
            
        if not dialogue_lines:
            log(f"    WARNING: No valid dialogue found!")
            return 0
        
        inserted = 0
        for line in dialogue_lines:
            doc = {
                'episode_title': title,
                'episode_number': number,
                'season': season,
                'season_name': season_name,
                'character': line['character'],
                'dialogue': line['dialogue'],
                'transcript': transcript_url,
                'image': image_url
            }
            collection.insert_one(doc)
            inserted += 1
        
        log(f"    SUCCESS: {inserted} dialogue lines inserted")
        return inserted
        
    except Exception as e:
        log(f"    ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 0


def main():
    log("=" * 60)
    log("BFDI Search - Database Population Script v8 (SMART PARSER)")
    log("=" * 60)
    log("Features:")
    log("  - Bold tag parsing for character names")
    log("  - 80+ known characters")
    log("  - Filters garbage/creator commentary")
    log("  - Strict dialogue validation")
    log("=" * 60)
    
    try:
        client.admin.command('ping')
        log("✓ Connected to MongoDB")
    except Exception as e:
        log(f"✗ MongoDB connection failed: {e}")
        return
    
    # Optionally clear existing data; otherwise keep and skip already-scraped episodes
    if CLEAR_EXISTING:
        log(f"\nClearing existing data for fresh scrape...")
        collection.delete_many({})
        log("✓ Collection cleared")
    else:
        log("\nPreserving existing data (CLEAR_EXISTING=False)")
    
    existing_episodes = get_existing_episodes() if SKIP_EPISODES_WITH_DATA else set()
    if SKIP_EPISODES_WITH_DATA:
        log(f"Will skip episodes already in DB ({len(existing_episodes)} found)")
    else:
        log("Will re-scrape all episodes (SKIP_EPISODES_WITH_DATA=False)")
    
    log(f"\nScraping {len(EPISODES)} episodes...\n")
    
    total_lines = 0
    successful = 0
    failed = 0
    failed_episodes = []
    
    for episode in EPISODES:
        if SKIP_EPISODES_WITH_DATA and episode['title'] in existing_episodes:
            log(f"    SKIP (already scraped): {episode['title']}")
            continue
        lines = scrape_episode(episode)
        
        if lines > 0:
            total_lines += lines
            successful += 1
        else:
            failed += 1
            failed_episodes.append(episode['title'])
        
        delay = BASE_DELAY + random.uniform(1.0, 3.0)
        time.sleep(delay)
    
    log("\n" + "=" * 60)
    log("SUMMARY")
    log("=" * 60)
    log(f"Episodes processed: {len(EPISODES)}")
    log(f"Successful: {successful}")
    log(f"Failed/No transcript: {failed}")
    log(f"Total dialogue lines: {total_lines}")
    log(f"Average lines per episode: {total_lines / max(successful, 1):.1f}")
    
    if failed_episodes:
        log(f"\nEpisodes without transcripts ({len(failed_episodes)}):")
        for ep in failed_episodes[:10]:
            log(f"  - {ep}")
        if len(failed_episodes) > 10:
            log(f"  ... and {len(failed_episodes) - 10} more")
    
    log("=" * 60)
    log(f"Log written to: {LOG_FILE}")


if __name__ == "__main__":
    main()
