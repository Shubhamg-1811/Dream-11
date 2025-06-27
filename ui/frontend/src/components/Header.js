// src/components/Header.js

import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Header.css'; // We'll create this CSS file later

function Header() {
  const location = useLocation();

  return (
    <header className="header">
      <div className="logo">Dream11 </div>
      <nav>
        <Link to="/" className={location.pathname === '/' ? 'active' : ''}>
          Team Selection
        </Link>
        <Link to="/model" className={location.pathname === '/model' ? 'active' : ''}>
          Model Analysis
        </Link>
      </nav>
    </header>
  );
}

export default Header;
