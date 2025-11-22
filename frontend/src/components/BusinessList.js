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

  const handleShare = async (e, business) => {
    e.stopPropagation();
    
    const shareText = `Check out ${business.name}!\n${business.formatted_address || business.vicinity}\n${business.rating ? `Rating: ${business.rating}⭐` : ''}`;
    const shareUrl = `https://www.google.com/maps/place/?q=place_id:${business.place_id}`;
    
    // Try native share API first (works on mobile)
    if (navigator.share) {
      try {
        await navigator.share({
          title: business.name,
          text: shareText,
          url: shareUrl
        });
        return;
      } catch (err) {
        if (err.name !== 'AbortError') {
          console.log('Share failed:', err);
        }
      }
    }
    
    // Fallback: Copy to clipboard
    const fullText = `${shareText}\n${shareUrl}`;
    try {
      await navigator.clipboard.writeText(fullText);
      alert('Business info copied to clipboard!');
    } catch (err) {
      // Final fallback: show info
      alert(`Share this business:\n\n${fullText}`);
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
            <div className="business-title-row">
              <h3>{business.name}</h3>
              <div className="business-actions">
                <button
                  className={`favorite-button ${favorites[business.place_id] ? 'favorited' : ''}`}
                  onClick={(e) => handleFavoriteToggle(e, business)}
                  title={favorites[business.place_id] ? 'Remove from favorites' : 'Add to favorites'}
                >
                  {favorites[business.place_id] ? '⭐' : '☆'}
                </button>
                <button
                  className="share-button"
                  onClick={(e) => handleShare(e, business)}
                  title="Share this business"
                >
                  📤
                </button>
              </div>
            </div>
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
