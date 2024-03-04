// Import necessary components from react-router-dom
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

// Import your page components
import WebApp from "./WebApp";
import RobotUI from "./RobotUI"; // Assume this is the new page you want to add

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<WebApp />} />
        <Route path="/robotui" element={<RobotUI />} />
      </Routes>
    </Router>
  );
}

export default App;
