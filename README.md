# 🏪 Small Business Finder

A React application that helps users discover small, local, independent businesses near them. The app uses Google Maps API for location data and Gemini AI to intelligently filter out chains and franchises, showing only authentic small businesses.

## Features

- 🔍 **Smart Search**: Enter what you're looking for (coffee shop, bookstore, etc.)
- 🤖 **AI-Powered Filtering**: Gemini AI filters out chains and franchises automatically
- 📍 **Location-Based**: Uses your current location or allows custom location
- 🗺️ **Interactive Map**: Google Maps integration with markers for each business
- 📱 **Responsive Design**: Works on desktop and mobile devices
- ⭐ **Business Details**: Ratings, addresses, opening hours, and more

## Tech Stack

### Frontend
- React 18
- Google Maps JavaScript API
- Axios for API calls
- CSS3 for styling

### Backend
- Node.js with Express
- Google Maps Places API
- Google Gemini AI API
- CORS enabled

## Prerequisites

Before you begin, you'll need:

1. **Node.js** (v14 or higher)
2. **Google Maps API Key** with the following APIs enabled:
   - Maps JavaScript API
   - Places API (Text Search)
3. **Google Gemini API Key**

## Getting Your API Keys

### Google Maps API Key
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable "Maps JavaScript API" and "Places API"
4. Go to Credentials → Create Credentials → API Key
5. Restrict your API key (recommended for production)

### Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Get API Key"
3. Create a new API key or use existing one

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd ElleHacks
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   
   Create/edit `.env` file in the root directory:
   ```env
   GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   PORT=5000
   ```

   Create/edit `.env.local` file in the root directory:
   ```env
   REACT_APP_GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
   ```

   **Important**: Replace `your_google_maps_api_key_here` and `your_gemini_api_key_here` with your actual API keys!

## Running the Application

### Development Mode (Both Frontend and Backend)

Run both the React frontend and Express backend simultaneously:

```bash
npm run dev
```

This will start:
- Backend server on `http://localhost:5000`
- React app on `http://localhost:3000`

### Run Separately

**Backend only:**
```bash
npm run server
```

**Frontend only:**
```bash
npm start
```

## Usage

1. Open your browser to `http://localhost:3000`
2. Allow location access when prompted (or it will use a default location)
3. Enter what you're looking for in the search bar (e.g., "coffee shop", "bookstore", "bakery")
4. Click "Search"
5. The app will:
   - Search Google Maps for relevant businesses
   - Use Gemini AI to filter out chains/franchises
   - Display only small, local businesses
6. Click on any business card to see its location on the map
7. Map markers are numbered and clickable

## Project Structure

```
ElleHacks/
├── public/
│   └── index.html
├── server/
│   └── server.js           # Express backend server
├── src/
│   ├── components/
│   │   ├── SearchBar.js    # Search input component
│   │   ├── SearchBar.css
│   │   ├── BusinessList.js # List of businesses
│   │   ├── BusinessList.css
│   │   ├── Map.js          # Google Maps component
│   │   └── Map.css
│   ├── App.js              # Main app component
│   ├── App.css
│   ├── index.js            # React entry point
│   └── index.css
├── .env                    # Backend environment variables
├── .env.local              # Frontend environment variables
├── .gitignore
├── package.json
└── README.md
```

## API Endpoints

### POST `/api/search`
Search for small businesses near a location.

**Request Body:**
```json
{
  "query": "coffee shop",
  "location": {
    "lat": 43.6532,
    "lng": -79.3832
  }
}
```

**Response:**
```json
{
  "success": true,
  "places": [...],
  "total": 5
}
```

### GET `/api/place/:placeId`
Get detailed information about a specific place.

### GET `/api/health`
Health check endpoint.

## How It Works

1. **User Input**: User enters a search query and their location is detected
2. **Google Maps Search**: Backend queries Google Places API for relevant businesses
3. **AI Filtering**: Gemini AI analyzes each business to determine if it's a small business or chain
4. **Results Display**: Only small businesses are returned and displayed
5. **Interactive Map**: Users can click on businesses to see them on the map

## Troubleshooting

### "Unable to load map" error
- Check that `REACT_APP_GOOGLE_MAPS_API_KEY` is set in `.env.local`
- Verify Maps JavaScript API is enabled in Google Cloud Console

### Backend connection errors
- Ensure backend is running on port 5000
- Check that `proxy` is set correctly in `package.json`

### No results found
- Try a different search term
- Check that your API keys are valid
- Check browser console and server logs for errors

### Gemini API errors
- Verify your Gemini API key is correct
- Check that you have quota remaining
- The app will fall back to showing all results if Gemini fails

## Future Enhancements

- [ ] Save favorite businesses
- [ ] User reviews and ratings
- [ ] Filter by distance, rating, or opening hours
- [ ] Share businesses with friends
- [ ] Business owner verification system

## Contributing

Feel free to fork this project and submit pull requests!

## License

MIT

## Support

If you encounter any issues, please check the troubleshooting section or open an issue on GitHub.