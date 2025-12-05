import { useState, useEffect } from 'react';
import axios from "axios";
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
  const [season, setSeason] = useState('');
  const [match, setMatch] = useState('');
  const [results, setResults] = useState([]);

  const [load, setLoad] = useState(false);
  const [show, setShow] = useState(false);
  const [modalMsg, setModalMsg] = useState('');


  /* UNUSED. For cosmetic purposes */
  /* Display a random hint when the image is clicked */
  /*const imageClicked = () => {
    let hint = hints[Math.floor(Math.random() * hints.length)];
    alert(`Spongebob fact: ${hint}\n(design still in progress)`);
  };*/

  const getResults = async () => {
    try {
      setLoad(true);
      // Specify search parameters
      let params = {};
      if (keywords) {
        params.keywords = keywords;
      }
      if (character) {
        params.character = character;
      }
      if (season) {
        params.season = season;
      }

      const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:3000';
      const response = await axios.get(`${backendUrl}/dialogue/search`, {
        params: params,
      });

      console.log("# of results:", response.data.length);
      //console.log("results:",response.data);
      
      setResults(response.data);
      setMatch(keywords);
      setLoad(false);
    } catch (e) {
      console.error(e);
      setMatch('');
      setLoad(false);
    }
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
                <Form.Control
                  as="select"
                  /*value={title}*/
                  onChange={(e) => setSeason(e.target.value)}
                >
                  <option value="">All</option>
                  {seasons.map((season) => (
                    <option key={season.id} value={season.id}>{season.name}</option>
                  ))}
                </Form.Control>
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
