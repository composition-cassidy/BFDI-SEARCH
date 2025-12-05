import { useState } from 'react'

import Pane from '../components/Pane'

function About() {
  return (
    <div className="app">
      <div className="aboutPane">
        <Pane>
          <h1>About</h1>
          <h2>What is BFDI Search?</h2>
          <p>
            <strong>BFDI Search</strong> is a web app that allows you to search across multiple episode transcripts of <strong>Battle for Dream Island</strong> (including the seasons of BFDIA, IDFB, BFB, and TPOT) for any key words or phrases.
            <br />
            It was built to help find specific clips for video editing, memes, or primarily sentence mixing..
          </p>
          <p>
            This project is based on SpongeSearch by CurtisTRY, adapted for the BFDI community.
            You can view SpongeSearch&apos;s source code{' '}
            <a href="https://github.com/curtistry/sponge-search/tree/main" target="_blank" rel="noopener noreferrer">
              here
            </a>
            .
          </p>
          <h2>Why was it built?</h2>
          <p>
            BFDI Search was built as a fan project inspired by SpongeSearch to make it easier to find certain words, phrases, quotes and moments from across the entire BFDI series.
          </p>
          <h2>How do I use this?</h2>
          <p>
            To use this web app, simply fill in the search form and it will display all occurrences of the dialogue based on your filters.
            <br/>
            Due to performance reasons, searches are limited to <b>150 results</b>.
          </p>
          <p>Each card in the list will display the following: </p>
          <ul>
          <li>Episode name</li>
          <li>Season (BFDI/BFDIA/IDFB/BFB/TPOT)</li>
          <li>Character (who said the line)</li>
          <li>The dialogue</li>
          <li>Title Card image (Desktop only)</li>
          </ul>
          <p>Clicking on the Title Card image will redirect you to the transcript page.</p>
          <h2>Missing episodes</h2>
          <p>The following episodes are currently not in the database due to HTML scraping issues:</p>
          <ul>
            <li>BFDIA 23: Shattered!</li>
            <li>BFDI:TPOT 14: I SAID CAREFUL!!!</li>
            <li>BFDI:TPOT 16: The Power of Four</li>
            <li>BFDI:TPOT 19: Last One Standing</li>
            <li>BFDI:TPOT 20: Last One Standing</li>
          </ul>
          <br />
          <b>This project is not affiliated with <i>jacknjellify</i> or the <i>BFDI Wiki</i>.</b>
        </Pane>
      </div>
    </div>
  )
}

export default About
