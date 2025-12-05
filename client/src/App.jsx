import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import logo from './assets/logo.png';

import { Nav, Navbar, Container } from 'react-bootstrap';
import {
  BrowserRouter as Router,
  Route, Routes, Link
} from "react-router-dom";

import Search from './pages/Search'
import About from './pages/About';

/*
* The main App comoponent. Consists of a navbar and a router.
*/
function App() {
  return (
    <Router>
      <Navbar expand="lg">
        <Container>
          <Navbar.Brand as={Link} to="/">
            <img src={logo} className="logo"/>
          </Navbar.Brand>
          <Nav className="me-auto">
            <Nav.Link as={Link} to="/search">Search</Nav.Link>
            <Nav.Link as={Link} to="/about">About</Nav.Link>
          </Nav>
        </Container>
      </Navbar>
      <div>
        <Routes>
          <Route index element={<Search />} />
          <Route path="search" element={<Search />} />
          <Route path="about" element={<About />} />
        </Routes>
      </div>

      <footer>
        <p>&copy; krasen m 2025. Based on SpongeSearch by Curtis.</p>
      </footer>
    </Router>
  )
}

export default App
