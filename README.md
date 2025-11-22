# 🏪 LocalMaps - Support Your Local Community

**LocalMaps** is a web application dedicated to helping people discover and support small, local, independent businesses in their community. By filtering out large chains and franchises, LocalMaps ensures that users find authentic local gems - from family-owned cafes and independent bookstores to local art galleries and community event spaces.

## 🎯 Our Mission

LocalMaps exists to:
- **Support Small Businesses**: Help local entrepreneurs get discovered by connecting them directly with customers in their area
- **Promote Local Arts**: Showcase independent galleries, artist studios, craft shops, and creative spaces that make communities unique
- **Highlight Community Events**: Connect people with local venues hosting farmers markets, craft fairs, live music, and community gatherings
- **Build Stronger Communities**: Keep money circulating locally and help neighborhoods maintain their unique character
- **Combat Big Chain Dominance**: Provide an alternative to generic search results dominated by corporate chains

Every search on LocalMaps helps a local business owner, a community artist, or a neighborhood gathering space thrive.

## ✨ Features

### User Features
- 🔍 **Smart Search**: Find local businesses, art spaces, or event venues by category
- 🤖 **AI-Powered Filtering**: Gemini AI automatically filters out chains and franchises
- 📍 **Location-Based Discovery**: Uses your current location or allows custom search areas
- 🗺️ **Interactive Map**: Google Maps integration with numbered markers for easy navigation
- 🔐 **User Accounts**: Register and login to save your favorite places
- ⭐ **Favorites Management**: Save and organize your favorite local spots
- 📤 **Share Businesses**: Share local gems with friends via link or clipboard
- 🎚️ **Advanced Filters**: Filter by distance (1-25km), minimum rating (3+, 4+, 4.5+), or open/closed status
- 🚀 **Quick Search**: One-click searches for popular categories (Coffee Shop, Restaurant, Bookstore, Bakery, Boutique)
- 📱 **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices

### Business Information
- ⭐ **Ratings & Reviews**: See Google ratings and review counts
- 📍 **Full Address**: Complete address information
- 🕐 **Opening Hours**: Real-time open/closed status
- 🏷️ **Business Categories**: View business types and specialties
- 🔗 **Direct Links**: One-click access to Google Maps for directions

## 🛠️ Technology Stack

### Frontend
- **Framework**: React 18.2.0
- **Maps Integration**: @googlemaps/js-api-loader 1.16.2
- **HTTP Client**: Axios 1.6.2
- **State Management**: React Context API for global auth state
- **Styling**: CSS3 with responsive design and modern animations

### Backend
- **Framework**: FastAPI 0.104.1 (Python)
- **Server**: Uvicorn 0.24.0 (ASGI)
- **Database**: SQLite3 for user accounts and favorites
- **HTTP Client**: httpx 0.25.2 (async)
- **Validation**: Pydantic 2.5.2 for request/response schemas
- **Environment**: python-dotenv 1.0.0

### External APIs
- **Google Maps Places API**: Text Search and Place Details
- **Google Gemini AI**: gemini-pro model for intelligent business filtering

### Security
- Password hashing with SHA-256
- Token-based authentication with 7-day session expiry
- CORS configured for secure frontend-backend communication
- API keys protected in environment variables

## 📋 Prerequisites

Before you begin, ensure you have:

1. **Python 3.8+** installed
2. **Node.js 14+** and npm installed
3. **Google Maps API Key** with these APIs enabled:
   - Maps JavaScript API
   - Places API (Text Search)
   - Place Details API
4. **Google Gemini API Key**

## 🔑 Getting Your API Keys

### Google Maps API Key
1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select an existing one)
3. Enable the following APIs:
   - **Maps JavaScript API**
   - **Places API**
4. Navigate to: Credentials → Create Credentials → API Key
5. Copy your API key
6. (Recommended) Restrict your API key for production use

### Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Get API Key"
3. Copy your API key

## 🚀 Quick Setup & Installation

### Step 1: Clone the Repository
```bash
git clone <your-repo-url>
cd ElleHacks
```

### Step 2: Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment:**
   - **Windows (PowerShell):**
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
   - **Windows (Command Prompt):**
     ```cmd
     .venv\Scripts\activate.bat
     ```
   - **Mac/Linux:**
     ```bash
     source .venv/bin/activate
     ```

4. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create `.env` file in the `backend` folder:**
   ```env
   GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   PORT=8000
   HOST=0.0.0.0
   ```
   
   **Important**: Replace the placeholder values with your actual API keys!

### Step 3: Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd ../frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Create `.env.local` file in the `frontend` folder:**
   ```env
   REACT_APP_GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
   ```
   
   **Important**: Use the SAME Google Maps API key as the backend!

### Step 4: Running the Application

You need to run both the backend and frontend servers:

#### Terminal 1 - Backend Server:
```bash
cd backend
.venv\Scripts\python.exe -m uvicorn main:app --reload
```

The backend will start on: `http://localhost:8000`

#### Terminal 2 - Frontend Server:
```bash
cd frontend
npm start
```

The frontend will start on: `http://localhost:3000`

**That's it!** Your browser should automatically open to `http://localhost:3000`

## 📖 How to Use LocalMaps

### First Time Setup
1. **Open your browser** to `http://localhost:3000`
2. **Allow location access** when prompted (or it will use Toronto as default)
3. **Create an account** (optional but recommended):
   - Click "Login / Register" in the header
   - Fill in username, email, and password
   - Click "Register"

### Searching for Local Businesses
1. **Enter a search query** in the search bar:
   - Examples: "coffee shop", "art gallery", "bookstore", "craft brewery", "vintage shop"
2. **Use quick search buttons** for popular categories:
   - Coffee Shop, Restaurant, Bookstore, Bakery, Boutique
3. **Apply filters** (optional):
   - **Distance**: Choose radius from 1km to 25km
   - **Minimum Rating**: Filter by 3+, 4+, or 4.5+ stars
   - **Open Now**: Toggle to see only currently open businesses
4. **Click "Search"**

### Viewing Results
- The app will:
  1. Search Google Maps for relevant businesses
  2. Use Gemini AI to filter out chains and franchises
  3. Display only small, local, independent businesses
- **Business cards** show:
  - Name, rating, and review count
  - Full address
  - Open/closed status
  - Business categories
  - Favorite star (⭐) and share button (📤)
- **Click any business card** to see it highlighted on the map
- **Click map markers** to view business details

### Managing Favorites
1. **Save favorites**: Click the star icon (☆) on any business card
2. **View favorites**: Click "⭐ Favorites" button in the header
3. **Remove favorites**: Click "Remove" in the favorites modal
4. **View on map**: Click "View" to see the business on the map

### Sharing Businesses
- Click the share icon (📤) on any business card
- On mobile: Opens native share dialog
- On desktop: Copies business info and Google Maps link to clipboard

## 📁 Project Structure

```
ElleHacks/
├── frontend/                    # React frontend application
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/          # React components
│   │   │   ├── Auth.js         # Login/Register modal
│   │   │   ├── SearchBar.js    # Search input with filters
│   │   │   ├── BusinessList.js # Business cards with favorites
│   │   │   ├── Favorites.js    # Favorites modal
│   │   │   └── Map.js          # Google Maps integration
│   │   ├── context/
│   │   │   └── AuthContext.js  # Global authentication state
│   │   ├── App.js              # Main application component
│   │   ├── App.css
│   │   ├── index.js            # React entry point
│   │   └── index.css
│   ├── .env.local              # Frontend environment variables
│   └── package.json
│
├── backend/                     # FastAPI backend application
│   ├── api/
│   │   └── routes/             # API endpoints
│   │       ├── search.py       # Business search routes
│   │       ├── health.py       # Health check
│   │       └── auth.py         # Authentication routes
│   ├── services/               # Business logic
│   │   ├── google_maps_service.py
│   │   └── gemini_service.py
│   ├── database/               # SQLite database
│   │   └── db.py              # Database operations
│   ├── models/
│   │   └── schemas.py         # Pydantic models
│   ├── config/
│   │   └── settings.py        # Configuration
│   ├── .env                   # Backend environment variables
│   ├── main.py                # FastAPI application
│   └── requirements.txt       # Python dependencies
│
├── ARCHITECTURE.md            # System architecture documentation
├── PROJECT_STATUS.md          # Project status and features
├── SETUP.md                   # Quick setup guide
├── README.md                  # This file
└── .gitignore
```

## 🔌 API Endpoints

### Search Endpoints
- **POST `/api/search`** - Search for small businesses
  - Request: `{ query, location: { lat, lng } }`
  - Response: `{ success, places[], total }`
- **GET `/api/place/{place_id}`** - Get detailed place information
- **GET `/api/health`** - Health check and API status

### Authentication Endpoints
- **POST `/api/auth/register`** - Register new user
- **POST `/api/auth/login`** - Login user
- **POST `/api/auth/logout`** - Logout user
- **GET `/api/auth/me`** - Get current user info

### Favorites Endpoints
- **GET `/api/auth/favorites`** - Get user's favorites
- **POST `/api/auth/favorites`** - Add place to favorites
- **DELETE `/api/auth/favorites/{place_id}`** - Remove favorite
- **GET `/api/auth/favorites/check/{place_id}`** - Check if favorited

### Documentation
- Interactive API docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## 🔄 How It Works

### Search Flow
1. **User enters search query** (e.g., "art gallery") with optional filters
2. **Frontend detects location** using browser geolocation API
3. **Request sent to backend** via Axios HTTP client
4. **Backend queries Google Maps** Places API for nearby businesses
5. **Gemini AI analyzes results** to identify and filter out chains/franchises
6. **AI returns only small businesses** based on:
   - Business name patterns (excludes "McDonald's", "Starbucks", etc.)
   - Corporate indicators (franchise language, chain characteristics)
   - Local/independent business markers
7. **Frontend applies filters** (distance, rating, open status)
8. **Results displayed** in business cards and on interactive map
9. **Users can save favorites** and share discoveries

### Authentication Flow
1. **User registers/logs in** via Auth modal
2. **Backend creates secure session** with token-based authentication
3. **Token stored** in browser localStorage
4. **Token sent** with all authenticated requests (favorites, profile)
5. **Session expires** after 7 days for security

### Data Flow Architecture
```
User → React Frontend → FastAPI Backend → Google Maps API
                              ↓
                      Gemini AI Filter
                              ↓
                      SQLite Database (Users/Favorites)
                              ↓
                      ← Small Businesses Only
                              ↓
                      Interactive Map Display
```

## 🐛 Troubleshooting

### API Key Issues
**Problem**: "GOOGLE_MAPS_API_KEY is not set" warning
- **Solution**: 
  - Verify `.env` file exists in `backend/` folder
  - Verify `.env.local` file exists in `frontend/` folder
  - Ensure no extra spaces around the `=` sign
  - Restart both backend and frontend servers after adding keys

### Map Not Loading
**Problem**: Blank map or "Unable to load map" error
- **Solution**:
  - Check that `REACT_APP_GOOGLE_MAPS_API_KEY` is set in `frontend/.env.local`
  - Verify "Maps JavaScript API" is enabled in Google Cloud Console
  - Clear browser cache and reload

### Backend Connection Errors
**Problem**: "Failed to search" or network errors
- **Solution**:
  - Ensure backend server is running: `cd backend && uvicorn main:app --reload`
  - Verify backend is on port 8000: `http://localhost:8000/docs`
  - Check that frontend proxy is set to `http://localhost:8000` in `package.json`

### No Search Results
**Problem**: Search returns empty results or error
- **Solution**:
  - Try a different search term (e.g., "coffee" instead of "coffee shop")
  - Verify both API keys are valid and have quota remaining
  - Check backend terminal for error messages
  - Look at browser console (F12) for frontend errors

### Google Maps API REQUEST_DENIED
**Problem**: "Google Maps API error: REQUEST_DENIED"
- **Solution**:
  - Ensure API key has no restrictions preventing localhost usage
  - Verify Places API is enabled in Google Cloud Console
  - Check that the API key in `.env` matches your Google Cloud Console key
  - Try creating a new unrestricted API key for development

### Gemini AI Errors
**Problem**: Gemini filtering not working
- **Solution**:
  - Verify Gemini API key is correct in `backend/.env`
  - Check that you have API quota remaining
  - The app will gracefully fall back to showing all results if Gemini fails

### Database Errors
**Problem**: Login/register or favorites not working
- **Solution**:
  - Check that `backend/database/app.db` was created automatically
  - Look for database initialization messages in backend terminal
  - Delete `app.db` and restart backend to recreate tables

### Frontend Won't Start
**Problem**: `npm start` fails with Exit Code 1
- **Solution**:
  - Delete `node_modules` and `package-lock.json`
  - Run `npm install` again
  - Check for port 3000 already in use
  - Try `npm audit fix` if there are dependency issues

### Backend Won't Start
**Problem**: Python or uvicorn errors
- **Solution**:
  - Ensure virtual environment is activated
  - Verify Python 3.8+ is installed: `python --version`
  - Reinstall dependencies: `pip install -r requirements.txt`
  - Check for syntax errors in backend files

## 🚀 Deployment

### Production Considerations
- **Frontend**: Build with `npm run build` → Deploy to Vercel, Netlify, or AWS S3
- **Backend**: Deploy FastAPI app to Railway, Render, AWS Lambda, or DigitalOcean
- **Database**: Migrate from SQLite to PostgreSQL for production use
- **Security**: 
  - Enable API key restrictions in Google Cloud Console
  - Use HTTPS for all connections
  - Set proper CORS origins
  - Use environment variables for all secrets
  - Implement rate limiting

## 🎯 Future Enhancements

### Planned Features
- [ ] Business owner accounts to claim and update listings
- [ ] User reviews and photo uploads
- [ ] Social features: follow friends, share favorite lists
- [ ] Event calendar for local events and markets
- [ ] "Support" badges for Black-owned, women-owned, LGBTQ+ businesses
- [ ] Multi-language support
- [ ] Push notifications for new businesses near you
- [ ] Mobile app (React Native)
- [ ] Advanced analytics for business owners
- [ ] Integration with local business directories

## 🤝 Contributing

We welcome contributions to help make LocalMaps even better! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes** and test thoroughly
4. **Commit your changes**: `git commit -m "Add some feature"`
5. **Push to the branch**: `git push origin feature/your-feature-name`
6. **Open a Pull Request**

### Contribution Ideas
- Add new search filters or sorting options
- Improve the AI filtering algorithm
- Add support for more business categories
- Enhance mobile responsiveness
- Add internationalization (i18n)
- Improve accessibility (a11y)
- Write tests (unit tests, integration tests)
- Update documentation

## 📄 License

This project is licensed under the MIT License - feel free to use, modify, and distribute this software.

## 💬 Support

If you encounter any issues:
1. Check the **Troubleshooting** section above
2. Review the [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
3. Look at backend logs in the terminal for error messages
4. Check browser console (F12) for frontend errors
5. Open an issue on GitHub with:
   - Description of the problem
   - Steps to reproduce
   - Error messages (from both frontend and backend)
   - Your environment (OS, browser, Python version, Node version)

## 🌟 Why LocalMaps Matters

In an age dominated by chain stores and corporate franchises, **LocalMaps makes it easy to choose local**. Every time you use this app to find a small business, art gallery, or community event space, you're:

- 💰 **Supporting local economies** - Money spent locally stays in the community
- 🎨 **Preserving unique culture** - Independent businesses give neighborhoods character
- 👥 **Building community** - Local businesses know their customers and create gathering spaces
- 🌱 **Promoting sustainability** - Local businesses often have smaller environmental footprints
- 💼 **Creating jobs** - Small businesses employ millions of people worldwide

**Choose local. Support small. Build community.**

---

Made with ❤️ for supporting local communities everywhere.