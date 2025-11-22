# Quick Setup Guide

## Step 1: Get Your API Keys

### Google Maps API Key
1. Visit: https://console.cloud.google.com/
2. Create a new project (or select existing)
3. Enable these APIs:
   - Maps JavaScript API
   - Places API
4. Go to Credentials → Create Credentials → API Key
5. Copy your API key

### Gemini API Key
1. Visit: https://makersuite.google.com/app/apikey
2. Click "Get API Key"
3. Copy your API key

## Step 2: Configure Environment Variables

### Edit `.env` file (for backend):
Replace the placeholder values:
```env
GOOGLE_MAPS_API_KEY=your_actual_google_maps_key
GEMINI_API_KEY=your_actual_gemini_key
PORT=5000
```

### Edit `.env.local` file (for frontend):
Replace the placeholder value:
```env
REACT_APP_GOOGLE_MAPS_API_KEY=your_actual_google_maps_key
```

**Important:** Use the SAME Google Maps API key in both files!

## Step 3: Run the Application

Open terminal and run:
```bash
npm run dev
```

This starts both the frontend (React) and backend (Express) servers.

- Frontend: http://localhost:3000
- Backend: http://localhost:5000

## Step 4: Test the App

1. Open browser to http://localhost:3000
2. Allow location access when prompted
3. Search for something like "coffee shop" or "bookstore"
4. See small businesses appear!

## Troubleshooting

### Map doesn't load?
- Check `.env.local` has the correct API key
- Verify "Maps JavaScript API" is enabled in Google Cloud Console

### No search results?
- Check `.env` has the correct API keys
- Look at the terminal for backend errors
- Open browser console (F12) for frontend errors

### "npm run dev" doesn't work?
- Make sure you ran `npm install` first
- Try running separately:
  - Terminal 1: `npm run server`
  - Terminal 2: `npm start`

## Need Help?

Check the full README.md for detailed documentation!
