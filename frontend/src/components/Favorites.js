import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import './Favorites.css';

function Favorites({ onClose, onSelectBusiness }) {
  const { getFavorites, removeFavorite } = useAuth();
  const [favorites, setFavorites] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadFavorites();
  }, []);

  const loadFavorites = async () => {
    setLoading(true);
    const favs = await getFavorites();
    setFavorites(favs);
    setLoading(false);
  };

  const handleRemove = async (placeId) => {
    const result = await removeFavorite(placeId);
    if (result.success) {
      setFavorites(favorites.filter(f => f.place_id !== placeId));
    }
  };

  const handleViewBusiness = (favorite) => {
    const placeData = typeof favorite.place_data === 'string' 
      ? JSON.parse(favorite.place_data) 
      : favorite.place_data;
    onSelectBusiness(placeData);
    onClose();
  };

  return (
    <div className="favorites-overlay" onClick={onClose}>
      <div className="favorites-modal" onClick={(e) => e.stopPropagation()}>
        <button className="favorites-close" onClick={onClose}>×</button>
        
        <h2>⭐ My Favorites</h2>
        
        {loading ? (
          <div className="favorites-loading">Loading favorites...</div>
        ) : favorites.length === 0 ? (
          <div className="favorites-empty">
            <p>No favorites yet!</p>
            <p>Click the star icon on any business to save it here.</p>
          </div>
        ) : (
          <div className="favorites-list">
            {favorites.map((favorite) => (
              <div key={favorite.id} className="favorite-item">
                <div className="favorite-info">
                  <h3>{favorite.place_name}</h3>
                  <p className="favorite-address">{favorite.place_address}</p>
                  {favorite.place_rating && (
                    <p className="favorite-rating">⭐ {favorite.place_rating}</p>
                  )}
                </div>
                <div className="favorite-actions">
                  <button 
                    onClick={() => handleViewBusiness(favorite)}
                    className="view-button"
                  >
                    View
                  </button>
                  <button 
                    onClick={() => handleRemove(favorite.place_id)}
                    className="remove-button"
                  >
                    Remove
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Favorites;
