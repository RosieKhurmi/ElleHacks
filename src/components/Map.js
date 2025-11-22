import React, { useEffect, useRef, useState } from 'react';
import { Loader } from '@googlemaps/js-api-loader';
import './Map.css';

function Map({ location, businesses, selectedBusiness, onSelectBusiness }) {
  const mapRef = useRef(null);
  const mapInstanceRef = useRef(null);
  const markersRef = useRef([]);
  const [mapError, setMapError] = useState('');

  useEffect(() => {
    const initMap = async () => {
      try {
        const loader = new Loader({
          apiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY || '',
          version: 'weekly',
        });

        await loader.load();

        if (mapRef.current && !mapInstanceRef.current) {
          mapInstanceRef.current = new window.google.maps.Map(mapRef.current, {
            center: location,
            zoom: 13,
            styles: [
              {
                featureType: 'poi.business',
                stylers: [{ visibility: 'off' }]
              }
            ]
          });

          // Add user location marker
          new window.google.maps.Marker({
            position: location,
            map: mapInstanceRef.current,
            icon: {
              path: window.google.maps.SymbolPath.CIRCLE,
              scale: 10,
              fillColor: '#4285F4',
              fillOpacity: 1,
              strokeColor: '#ffffff',
              strokeWeight: 2,
            },
            title: 'Your Location'
          });
        }
      } catch (error) {
        console.error('Error loading map:', error);
        setMapError('Unable to load map. Please check your API key.');
      }
    };

    if (location) {
      initMap();
    }
  }, [location]);

  // Update map when businesses change
  useEffect(() => {
    if (mapInstanceRef.current && businesses.length > 0) {
      // Clear existing markers
      markersRef.current.forEach(marker => marker.setMap(null));
      markersRef.current = [];

      // Add markers for businesses
      const bounds = new window.google.maps.LatLngBounds();
      bounds.extend(location);

      businesses.forEach((business, index) => {
        if (business.geometry && business.geometry.location) {
          const position = {
            lat: business.geometry.location.lat,
            lng: business.geometry.location.lng
          };

          const marker = new window.google.maps.Marker({
            position: position,
            map: mapInstanceRef.current,
            title: business.name,
            label: {
              text: (index + 1).toString(),
              color: 'white',
              fontWeight: 'bold'
            },
            animation: window.google.maps.Animation.DROP
          });

          // Add click listener
          marker.addListener('click', () => {
            onSelectBusiness(business);
          });

          markersRef.current.push(marker);
          bounds.extend(position);
        }
      });

      // Fit map to show all markers
      mapInstanceRef.current.fitBounds(bounds);
    }
  }, [businesses, location, onSelectBusiness]);

  // Highlight selected business
  useEffect(() => {
    if (selectedBusiness && mapInstanceRef.current) {
      markersRef.current.forEach((marker, index) => {
        if (businesses[index]?.place_id === selectedBusiness.place_id) {
          marker.setAnimation(window.google.maps.Animation.BOUNCE);
          setTimeout(() => marker.setAnimation(null), 2000);
          
          mapInstanceRef.current.panTo(marker.getPosition());
          mapInstanceRef.current.setZoom(15);
        }
      });
    }
  }, [selectedBusiness, businesses]);

  return (
    <div className="map-container">
      {mapError && <div className="map-error">{mapError}</div>}
      <div ref={mapRef} className="map"></div>
    </div>
  );
}

export default Map;
