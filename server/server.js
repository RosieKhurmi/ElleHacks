const express = require('express');
const cors = require('cors');
const axios = require('axios');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

// Endpoint to search for places using Google Maps API
app.post('/api/search', async (req, res) => {
  try {
    const { query, location } = req.body;
    
    if (!query || !location) {
      return res.status(400).json({ error: 'Query and location are required' });
    }

    // First, get places from Google Maps Places API (Text Search)
    const placesResponse = await axios.post(
      `https://maps.googleapis.com/maps/api/place/textsearch/json?key=${process.env.GOOGLE_MAPS_API_KEY}`,
      null,
      {
        params: {
          query: `${query} near ${location.lat},${location.lng}`,
          radius: 5000, // 5km radius
          key: process.env.GOOGLE_MAPS_API_KEY
        }
      }
    );

    if (placesResponse.data.status !== 'OK' && placesResponse.data.status !== 'ZERO_RESULTS') {
      throw new Error(`Google Maps API error: ${placesResponse.data.status}`);
    }

    const places = placesResponse.data.results || [];

    // Use Gemini API to filter for small businesses
    const filteredPlaces = await filterSmallBusinesses(places, query);

    res.json({
      success: true,
      places: filteredPlaces,
      total: filteredPlaces.length
    });

  } catch (error) {
    console.error('Search error:', error.message);
    res.status(500).json({ 
      error: 'Failed to search for places',
      details: error.message 
    });
  }
});

// Function to filter small businesses using Gemini API
async function filterSmallBusinesses(places, searchQuery) {
  if (!places || places.length === 0) {
    return [];
  }

  try {
    // Prepare the data for Gemini
    const placesInfo = places.map((place, idx) => ({
      id: idx,
      name: place.name,
      address: place.formatted_address,
      types: place.types,
      rating: place.rating,
      user_ratings_total: place.user_ratings_total
    }));

    // Call Gemini API to filter for small businesses
    const geminiResponse = await axios.post(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${process.env.GEMINI_API_KEY}`,
      {
        contents: [{
          parts: [{
            text: `You are an expert at identifying small businesses vs chains/franchises. 
            
Given this list of places for the search "${searchQuery}", identify which ones are likely SMALL, LOCAL, INDEPENDENT businesses (not chains or franchises).

Places:
${JSON.stringify(placesInfo, null, 2)}

Return ONLY a JSON array of the IDs (just the numbers) of places that are small businesses. Consider:
- Local, independent establishments are small businesses
- Chain restaurants, franchises, big box stores are NOT small businesses
- Family-owned shops, local cafes, independent stores ARE small businesses
- Well-known national/international brands are NOT small businesses

Return format: [0, 2, 5] (just the array of ID numbers that are small businesses)
Return ONLY the array, no other text.`
          }]
        }]
      }
    );

    // Parse Gemini response
    const geminiText = geminiResponse.data?.candidates?.[0]?.content?.parts?.[0]?.text || '[]';
    
    // Extract the array from the response
    let smallBusinessIds = [];
    try {
      const match = geminiText.match(/\[[\d,\s]*\]/);
      if (match) {
        smallBusinessIds = JSON.parse(match[0]);
      }
    } catch (parseError) {
      console.error('Error parsing Gemini response:', parseError);
      // If Gemini fails, return all places as fallback
      return places;
    }

    // Filter the original places based on Gemini's selection
    const filteredPlaces = smallBusinessIds
      .map(id => places[id])
      .filter(place => place !== undefined);

    return filteredPlaces.length > 0 ? filteredPlaces : places.slice(0, 5); // Fallback to first 5

  } catch (error) {
    console.error('Gemini filtering error:', error.message);
    // If filtering fails, return all places
    return places;
  }
}

// Endpoint to get place details
app.get('/api/place/:placeId', async (req, res) => {
  try {
    const { placeId } = req.params;
    
    const detailsResponse = await axios.get(
      `https://maps.googleapis.com/maps/api/place/details/json`,
      {
        params: {
          place_id: placeId,
          key: process.env.GOOGLE_MAPS_API_KEY
        }
      }
    );

    res.json(detailsResponse.data);

  } catch (error) {
    console.error('Place details error:', error.message);
    res.status(500).json({ 
      error: 'Failed to get place details',
      details: error.message 
    });
  }
});

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', message: 'Server is running' });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`Google Maps API Key: ${process.env.GOOGLE_MAPS_API_KEY ? 'Set' : 'Not set'}`);
  console.log(`Gemini API Key: ${process.env.GEMINI_API_KEY ? 'Set' : 'Not set'}`);
});
