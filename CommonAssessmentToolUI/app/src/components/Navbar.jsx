import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./Navbar.css";

const Navbar = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const navigate = useNavigate();

  const handleSearchChange = (event) => {
    setSearchQuery(event.target.value);
  };

  const handleSearchSubmit = (event) => {
    event.preventDefault();
    if (searchQuery) {
      navigate(`/clients?query=${encodeURIComponent(searchQuery)}`);
    }
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <Link to="/">Case Management Tool</Link>
        </div>
        {/* <ul className="navbar-nav">
          <li className="nav-item">
            <Link to="/about">About</Link>
          </li>
          <li className="nav-item">
            <Link to="/predictions">Predictions</Link>
          </li>
        </ul> */}
        <form className="nav-search" onSubmit={handleSearchSubmit}>
          <input
            type="text"
            placeholder="Search..."
            aria-label="Search"
            value={searchQuery}
            onChange={handleSearchChange}
          />
          <button type="submit">Go</button>
        </form>
      </div>
    </nav>
  );
};

export default Navbar;
