import { useState, useEffect } from 'react';
import Pane from '../components/Pane'
import ResultCard from '../components/ResultCard';

import { Button, Form, Modal } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

// BFDI Character list
const characters = [
  // Hosts
  { id: 'announcer', name: 'Announcer' },
  { id: 'four', name: 'Four' },
  { id: 'two', name: 'Two' },
  { id: 'x', name: 'X' },
  // Main contestants
  { id: 'leafy', name: 'Leafy' },
  { id: 'firey', name: 'Firey' },
  { id: 'bubble', name: 'Bubble' },
  { id: 'pencil', name: 'Pencil' },
  { id: 'match', name: 'Match' },
  { id: 'ice cube', name: 'Ice Cube' },
  { id: 'pen', name: 'Pen' },
  { id: 'eraser', name: 'Eraser' },
  { id: 'blocky', name: 'Blocky' },
  { id: 'snowball', name: 'Snowball' },
  { id: 'golf ball', name: 'Golf Ball' },
  { id: 'tennis ball', name: 'Tennis Ball' },
  { id: 'coiny', name: 'Coiny' },
  { id: 'pin', name: 'Pin' },
  { id: 'needle', name: 'Needle' },
  { id: 'teardrop', name: 'Teardrop' },
  { id: 'rocky', name: 'Rocky' },
  { id: 'woody', name: 'Woody' },
  { id: 'flower', name: 'Flower' },
  { id: 'spongy', name: 'Spongy' },
  { id: 'david', name: 'David' },
  { id: 'dora', name: 'Dora' },
  // BFB/TPOT characters
  { id: 'lollipop', name: 'Lollipop' },
  { id: 'gelatin', name: 'Gelatin' },
  { id: 'donut', name: 'Donut' },
  { id: 'barf bag', name: 'Barf Bag' },
  { id: 'taco', name: 'Taco' },
  { id: 'saw', name: 'Saw' },
  { id: 'book', name: 'Book' },
  { id: 'ruby', name: 'Ruby' },
  { id: 'fries', name: 'Fries' },
  { id: 'puffball', name: 'Puffball' },
  { id: 'yellow face', name: 'Yellow Face' },
  { id: 'black hole', name: 'Black Hole' },
  { id: 'tree', name: 'Tree' },
  { id: 'bottle', name: 'Bottle' },
  { id: 'pie', name: 'Pie' },
  { id: 'loser', name: 'Loser' },
  { id: 'winner', name: 'Winner' },
]

// BFDI Season list
const seasons = [
  { id: 1, name: 'BFDI (Season 1)' },
  { id: 2, name: 'BFDIA (Season 2)' },
  { id: 3, name: 'IDFB (Season 3)' },
  { id: 4, name: 'BFB (Season 4)' },
  { id: 5, name: 'TPOT (Season 5)' },
]


function Search() {

  const [keywords, setKeywords] = useState('');
  const [character, setCharacter] = useState('');
  const [selectedSeasons, setSelectedSeasons] = useState([]);
  const [exactMatch, setExactMatch] = useState(false);
  const [match, setMatch] = useState('');
  const [results, setResults] = useState([]);
  const [dialogue, setDialogue] = useState([]);
  const [thumbIndex, setThumbIndex] = useState({});
  const [thumbSlugIndex, setThumbSlugIndex] = useState({});
  const [thumbReady, setThumbReady] = useState(false);
  const [dataError, setDataError] = useState('');

  const [load, setLoad] = useState(false);
  const [show, setShow] = useState(false);
  const [modalMsg, setModalMsg] = useState('');


  /* UNUSED. For cosmetic purposes */
  /* Display a random hint when the image is clicked */
  /*const imageClicked = () => {
    let hint = hints[Math.floor(Math.random() * hints.length)];
    alert(`Spongebob fact: ${hint}\n(design still in progress)`);
  };*/

  useEffect(() => {
    const load = async () => {
      try {
        const [dialogueRes, thumbRes] = await Promise.all([
          fetch('/dialogue_export.json'),
          fetch('/thumbnails/index.json')
        ]);

        if (!dialogueRes.ok) throw new Error(`dialogue_export.json HTTP ${dialogueRes.status}`);
        if (!thumbRes.ok) throw new Error(`thumbnails/index.json HTTP ${thumbRes.status}`);

        const data = await dialogueRes.json();
        const thumbs = await thumbRes.json();
        setDialogue(Array.isArray(data) ? data : []);
        const safeThumbs = thumbs && typeof thumbs === 'object' ? thumbs : {};
        setThumbIndex(safeThumbs);

        // Build a slug map for fuzzy matching (lowercase, non-alnum -> underscore).
        const slugMap = {};
        const slugify = (str) =>
          (str || '')
            .toLowerCase()
            .replace(/[^a-z0-9]+/g, '_')
            .replace(/^_+|_+$/g, '');
        for (const [k, v] of Object.entries(safeThumbs)) {
          if (v && v.filename) {
            slugMap[slugify(k)] = v.filename;
          }
        }
        setThumbSlugIndex(slugMap);
        setThumbReady(true);
      } catch (err) {
        console.error('Failed to load dialogue_export.json', err);
        setDataError('Failed to load dialogue data.');
      }
    };
    load();
  }, []);

  const findThumb = (title) => {
    const key = (title || '').trim();
    const direct = thumbIndex[key];
    if (direct && direct.filename) return direct.filename;
    const lower = key.toLowerCase();
    for (const [k, v] of Object.entries(thumbIndex)) {
      if (k.toLowerCase() === lower && v && v.filename) {
        return v.filename;
      }
    }
    const slugify = (str) =>
      (str || '')
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, '_')
        .replace(/^_+|_+$/g, '');
    const slug = slugify(key);
    if (thumbSlugIndex[slug]) return thumbSlugIndex[slug];
    return null;
  };

  // If thumbnails load after an initial search, refresh results to attach thumbnails.
  useEffect(() => {
    if (thumbReady && keywords.length >= 2 && dialogue.length) {
      getResults();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [thumbReady]);

  const getResults = () => {
    setLoad(true);
    const keywordTerm = keywords.trim();
    const escapeRegex = (str) => str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const filtered = dialogue.filter((d) => {
      if (selectedSeasons.length > 0 && !selectedSeasons.includes(String(d.season))) return false;
      if (character) {
        const hay = (d.character || '').toLowerCase();
        if (!hay.includes(character.toLowerCase())) return false;
      }
      if (keywordTerm) {
        const hayRaw = d.dialogue || '';
        // Ignore parenthetical stage directions when matching.
        const hay = hayRaw.replace(/\([^)]*\)/g, '');
        if (exactMatch) {
          const pattern = new RegExp(`\\b${escapeRegex(keywordTerm)}\\b`, 'i');
          if (!pattern.test(hay)) return false;
        } else {
          if (!hay.toLowerCase().includes(keywordTerm.toLowerCase())) return false;
        }
      }
      return true;
    });
    const withThumb = filtered.map((d) => {
      const filename = findThumb(d.episode_title);
      return {
        ...d,
        thumbnail: filename ? `/thumbnails/${filename}` : `/thumbnails/placeholder.jpg`,
      };
    });
    setResults(withThumb.slice(0, 150));
    setMatch(keywords);
    setLoad(false);
  }

  // Method to handle search/filter submissions.
  const handleSubmit = () => {

    // Check if no keywords were specified.
    if (keywords.length < 2){
      console.error("The keyword should be at least 2 characters.");
      setMatch('');
      setResults([]);
      return;
    }
    if (dataError || !dialogue.length) {
      setModalMsg(dataError || 'Dialogue data not loaded yet. Please try again in a moment.');
      setShow(true);
      return;
    }
    // Send search and filter data to the Backend API. 
    getResults();

  }

  // Method to handle modal closing.
  const handleClose = () => {
    setModalMsg("");
    setShow(false);
  }

  return (
    <div>
      <div className="app">
        {/* Sidebar */}
        <div className="sidebar">
          <Pane>
            <h3>Search & Filter</h3>
            <Form>
              <Form.Group className="mb-3">
                <Form.Label>Keywords/Phrases</Form.Label>
                <Form.Control
                  as="textarea"
                  rows={2}
                  placeholder="Enter key words or phrases"
                  /*value={title}*/
                  onChange={(e) => setKeywords(e.target.value.toLowerCase())}
                />
                <Form.Check
                  className="mt-2"
                  type="checkbox"
                  label="Exact word/phrase match"
                  checked={exactMatch}
                  onChange={(e) => setExactMatch(e.target.checked)}
                />
              </Form.Group>
              <Form.Group>
                <Form.Label>Character</Form.Label>
                <Form.Control
                  as="select"
                  /*value={title}*/
                  onChange={(e) => setCharacter(e.target.value)}
                >
                  <option value="">All</option>
                  {characters.map((char) => (
                    <option key={char.id} value={char.id}>{char.name}</option>
                  ))}
                </Form.Control>
              </Form.Group>
              <br />
              <Form.Group>
                <Form.Label>Season</Form.Label>
                {seasons.map((season) => (
                  <Form.Check
                    key={season.id}
                    type="checkbox"
                    label={season.name}
                    checked={selectedSeasons.includes(String(season.id))}
                    onChange={(e) => {
                      const value = String(season.id);
                      setSelectedSeasons((prev) =>
                        e.target.checked
                          ? [...prev, value]
                          : prev.filter((s) => s !== value)
                      );
                    }}
                  />
                ))}
              </Form.Group>
              <br />
              <Button variant="primary" type="button" onClick={handleSubmit} disabled={load}> 
                {load ? "Loading" : "Search"}
              </Button>
            </Form>

          </Pane>
        </div>
        {/* Results pane */}
        <div className='resultsPane'>
          <Pane>
            <h3>Results <span id="no-custom-font">({results.length})</span></h3>
            <div className='resultsList'>
              {results.length > 0 ?
                results.map((result) => (
                  <ResultCard result={result} highlight={match} />
                ))
                : <p>
                  <b>No results found.</b>
                  <br />
                  Try modifying your keywords, character, or season.
                </p>}
            </div>
          </Pane>
        </div>
      </div>

      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Message</Modal.Title>
        </Modal.Header>
        <Modal.Body>{modalMsg}</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            OK
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  )
}

export default Search
