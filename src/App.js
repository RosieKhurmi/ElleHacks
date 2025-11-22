import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Loader } from '@googlemaps/js-api-loader';
import SearchBar from './components/SearchBar';
import BusinessList from './components/BusinessList';
import Map from './components/Map';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [location, setLocation] = useState(null);
  const [businesses, setBusinesses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedBusiness, setSelectedBusiness] = useState(null);

  // Get user's current location on mount
  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setLocation({
            lat: position.coords.latitude,
            lng: position.coords.longitude
          });
        },
        (error) => {
          console.error('Error getting location:', error);
          // Default to a location (e.g., Toronto)
          setLocation({ lat: 43.6532, lng: -79.3832 });
        }
      );
    } else {
      // Default location if geolocation not supported
      setLocation({ lat: 43.6532, lng: -79.3832 });
    }
  }, []);

  const handleSearch = async (searchQuery) => {
    if (!searchQuery.trim() || !location) {
      setError('Please enter a search query');
      return;
    }

    setLoading(true);
    setError('');
    setBusinesses([]);
    setSelectedBusiness(null);

    try {
      const response = await axios.post('/api/search', {
        query: searchQuery,
        location: location
      });

      if (response.data.success) {
        setBusinesses(response.data.places);
        if (response.data.places.length === 0) {
          setError('No small businesses found. Try a different search.');
        }
      } else {
        setError('Search failed. Please try again.');
      }
    } catch (err) {
      console.error('Search error:', err);
      setError('Failed to search. Please check your connection and try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🏪 Small Business Finder</h1>
        <p>Discover local, independent businesses near you</p>
      </header>

      <div className="content">
        <SearchBar 
          onSearch={handleSearch}
          loading={loading}
        />

        {error && <div className="error-message">{error}</div>}

        <div className="main-content">
          <div className="results-section">
            {loading && (
              <div className="loading">
                <div className="spinner"></div>
                <p>Searching for small businesses...</p>
              </div>
            )}

            {!loading && businesses.length > 0 && (
              <>
                <h2>Found {businesses.length} Small Businesses</h2>
                <BusinessList 
                  businesses={businesses}
                  selectedBusiness={selectedBusiness}
                  onSelectBusiness={setSelectedBusiness}
                />
              </>
            )}
          </div>

          <div className="map-section">
            {location && (
              <Map 
                location={location}
                businesses={businesses}
                selectedBusiness={selectedBusiness}
                onSelectBusiness={setSelectedBusiness}
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
