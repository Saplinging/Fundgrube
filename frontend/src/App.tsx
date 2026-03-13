
import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Upload from "./Upload";
import Chat from "./Chat";

const App: React.FC = () => {
  return (
    <Router>
      <nav style={{ display: "flex", gap: 16, padding: 16 }}>
        <Link to="/upload">Upload</Link>
        <Link to="/chat">Chat</Link>
      </nav>
      <Routes>
        <Route path="/upload" element={<Upload />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="/" element={<div style={{ padding: 16 }}><h1>Willkommen zu Fundgrube</h1></div>} />
      </Routes>
    </Router>
  );
};

export default App;
