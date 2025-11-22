import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import './BusinessList.css';

function BusinessList({ businesses, selectedBusiness, onSelectBusiness }) {
  const { addFavorite, removeFavorite, checkFavorite, isAuthenticated } = useAuth();
  const [favorites, setFavorites] = useState({});
  
  useEffect(() => {
    if (isAuthenticated) {
      businesses.forEach(async (business) => {
        const isFav = await checkFavorite(business.place_id);
        setFavorites(prev => ({ ...prev, [business.place_id]: isFav }));
      });
    } else {
      setFavorites({});
    }
  }, [businesses, isAuthenticated]);
  
  const handleFavoriteToggle = async (e, business) => {
    e.stopPropagation();
    
    if (!isAuthenticated) {
      alert('Please login to save favorites');
      return;
    }
    
    const isFav = favorites[business.place_id];
    
    if (isFav) {
      const result = await removeFavorite(business.place_id);
      if (result.success) {
        setFavorites(prev => ({ ...prev, [business.place_id]: false }));
      }
    } else {
      const result = await addFavorite(business);
      if (result.success) {
        setFavorites(prev => ({ ...prev, [business.place_id]: true }));
      } else {
        alert(result.error || 'Failed to add favorite');
      }
    }
  };
  return (
    <div className="business-list">
      {businesses.map((business, index) => (
        <div
          key={business.place_id || index}
          className={`business-card ${selectedBusiness?.place_id === business.place_id ? 'selected' : ''}`}
          onClick={() => onSelectBusiness(business)}
        >
          <div className="business-header">
            <h3>{business.name}</h3>
            <button
              className={`favorite-button ${favorites[business.place_id] ? 'favorited' : ''}`}
              onClick={(e) => handleFavoriteToggle(e, business)}
              title={favorites[business.place_id] ? 'Remove from favorites' : 'Add to favorites'}
            >
              {favorites[business.place_id] ? '⭐' : '☆'}
            </button>
            {business.rating && (
              <div className="rating">
                ⭐ {business.rating}
                {business.user_ratings_total && (
                  <span className="rating-count"> ({business.user_ratings_total})</span>
                )}
              </div>
            )}
          </div>

          <p className="address">{business.formatted_address || business.vicinity}</p>

          {business.opening_hours && (
            <p className={`status ${business.opening_hours.open_now ? 'open' : 'closed'}`}>
              {business.opening_hours.open_now ? '🟢 Open now' : '🔴 Closed'}
            </p>
          )}

          {business.types && business.types.length > 0 && (
            <div className="types">
              {business.types.slice(0, 3).map((type, idx) => (
                <span key={idx} className="type-badge">
                  {type.replace(/_/g, ' ')}
                </span>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

export default BusinessList;
