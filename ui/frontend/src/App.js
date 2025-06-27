// src/App.js

import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "./components/Header"; 
import ProductUI from "./components/ProductUI";
import ModelUI from "./components/ModelUI";
import "./App.css"; 

function App() {
  return (
    <Router>
      <Header />
      <div className="app-container">
        <Routes>
          <Route path="/" element={<ProductUI />} />
          <Route path="/model" element={<ModelUI />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
