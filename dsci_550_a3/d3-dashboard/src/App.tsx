import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import BubbleMap from './pages/BubbleMap';
import RadialChartPage from './pages/RadialChartPage';
import CirclePackingPage from './pages/CirclePackingPage'; // ✅ ADD THIS
import HomePage from './pages/HomePage';
import ScatterplotPage from './pages/ScatterplotPage';  // import it at the top


function App() {
  return (
    <Router>
      <header style={{
        position: "fixed",
        top: 0,
        width: "100%",
        backgroundColor: "#f9f9f9",
        padding: "15px 30px",
        display: "flex",
        justifyContent: "center",
        gap: "40px",
        borderBottom: "1px solid #ccc",
        zIndex: 1000
      }}>
        <Link to="/" style={{ fontSize: "18px", textDecoration: "none", color: "#3b82f6" }}>Home</Link>
        <Link to="/bubble" style={{ fontSize: "18px", textDecoration: "none", color: "#3b82f6" }}>Bubble Map</Link>
        <Link to="/radial" style={{ fontSize: "18px", textDecoration: "none", color: "#3b82f6" }}>Radial Chart</Link>
        <Link to="/circlepacking" style={{ fontSize: "18px", textDecoration: "none", color: "#3b82f6" }}>Circle Packing</Link>
        <Link to="/scatter" style={{ fontSize: "18px", textDecoration: "none", color: "#3b82f6" }}>Scatterplot</Link>

      <a
        href='https://danrobocrop.pythonanywhere.com/'
        target="_blank"
        rel="noopener noreferrer"
        style ={{ fontSize: "18px", textDecoration: "none", color: "#3b82f6" }}
      >
        Flight Visualization
      </a>
      </header>

      <main style={{ paddingTop: "100px" }}>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/bubble" element={<BubbleMap />} />
          <Route path="/radial" element={<RadialChartPage />} />
          <Route path="/circlepacking" element={<CirclePackingPage />} />
          <Route path="/scatter" element={<ScatterplotPage />} />

        </Routes>
      </main>
    </Router>
  );
}

export default App;
