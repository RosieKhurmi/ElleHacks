import React, { useState } from 'react';
import './SearchBar.css';

function SearchBar({ onSearch, loading }) {
  const [query, setQuery] = useState('');
  const [radius, setRadius] = useState('5000');
  const [minRating, setMinRating] = useState('0');
  const [openNow, setOpenNow] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(query, { radius, minRating, openNow });
  };

  const quickSearches = ['Coffee Shop', 'Restaurant', 'Bookstore', 'Bakery', 'Boutique'];

  return (
    <div className="search-bar">
      <form onSubmit={handleSubmit}>
        <div className="search-input-container">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="What are you looking for? (e.g., coffee shop, bookstore, bakery)"
            disabled={loading}
            className="search-input"
          />
          <button 
            type="submit" 
            disabled={loading || !query.trim()}
            className="search-button"
          >
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>

        <div className="filters-container">
          <div className="filter-group">
            <label htmlFor="radius">Distance:</label>
            <select 
              id="radius"
              value={radius} 
              onChange={(e) => setRadius(e.target.value)}
              disabled={loading}
              className="filter-select"
            >
              <option value="1000">1 km</option>
              <option value="2000">2 km</option>
              <option value="5000">5 km</option>
              <option value="10000">10 km</option>
              <option value="25000">25 km</option>
            </select>
          </div>

          <div className="filter-group">
            <label htmlFor="rating">Min Rating:</label>
            <select 
              id="rating"
              value={minRating} 
              onChange={(e) => setMinRating(e.target.value)}
              disabled={loading}
              className="filter-select"
            >
              <option value="0">Any</option>
              <option value="3">3+ ⭐</option>
              <option value="4">4+ ⭐</option>
              <option value="4.5">4.5+ ⭐</option>
            </select>
          </div>

          <div className="filter-group checkbox-group">
            <label>
              <input
                type="checkbox"
                checked={openNow}
                onChange={(e) => setOpenNow(e.target.checked)}
                disabled={loading}
              />
              <span>Open Now</span>
            </label>
          </div>
        </div>

        <div className="quick-searches">
          <span className="quick-label">Quick Search:</span>
          {quickSearches.map((search) => (
            <button
              key={search}
              type="button"
              className="quick-button"
              onClick={() => {
                setQuery(search);
                onSearch(search, { radius, minRating, openNow });
              }}
              disabled={loading}
            >
              {search}
            </button>
          ))}
        </div>
      </form>
    </div>
  );
}

export default SearchBar;
