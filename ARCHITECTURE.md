# LocalMaps Architecture

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER INTERFACE                                  │
│                           React App (Port 3000)                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ HTTP/REST API
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          FRONTEND (React 18.2.0)                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌─────────────────┐        ┌──────────────────┐                            │
│  │  Components     │        │   Context         │                            │
│  ├─────────────────┤        ├──────────────────┤                            │
│  │ • App.js        │◄───────┤ • AuthContext.js │                            │
│  │ • SearchBar     │        │   (Global Auth)  │                            │
│  │ • BusinessList  │        └──────────────────┘                            │
│  │ • Map           │                                                         │
│  │ • Auth (Login)  │                                                         │
│  │ • Favorites     │                                                         │
│  └─────────────────┘                                                         │
│                                                                               │
│  Features:                                                                   │
│  • Geolocation detection                                                     │
│  • Search with filters (distance, rating, open now)                         │
│  • Google Maps integration (@googlemaps/js-api-loader)                      │
│  • User authentication (login/register)                                     │
│  • Favorites management                                                     │
│  • Business sharing (clipboard/native share)                                │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ Axios HTTP Client
                                    │ Proxy: http://localhost:8000
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         BACKEND (FastAPI + Python)                           │
│                              Port 8000                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌───────────────────────────────────────────────────────────────────┐      │
│  │                         API ROUTES                                 │      │
│  ├───────────────────────────────────────────────────────────────────┤      │
│  │                                                                     │      │
│  │  /api/search (POST)          - Search for small businesses         │      │
│  │  /api/place/{id} (GET)       - Get place details                  │      │
│  │  /api/health (GET)           - Health check                        │      │
│  │                                                                     │      │
│  │  /api/auth/register (POST)   - Register new user                  │      │
│  │  /api/auth/login (POST)      - Login user                         │      │
│  │  /api/auth/logout (POST)     - Logout user                        │      │
│  │  /api/auth/me (GET)          - Get current user                   │      │
│  │  /api/auth/favorites (GET/POST/DELETE) - Manage favorites         │      │
│  │                                                                     │      │
│  └───────────────────────────────────────────────────────────────────┘      │
│                           │                    │                             │
│                           ▼                    ▼                             │
│  ┌─────────────────────────────┐    ┌──────────────────────┐               │
│  │       SERVICES              │    │   DATABASE           │               │
│  ├─────────────────────────────┤    ├──────────────────────┤               │
│  │                             │    │  SQLite (app.db)     │               │
│  │ • google_maps_service.py    │    │                      │               │
│  │   - search_places()         │    │  Tables:             │               │
│  │   - get_place_details()     │    │  • users             │               │
│  │                             │    │  • sessions          │               │
│  │ • gemini_service.py         │    │  • favorites         │               │
│  │   - filter_small_businesses │    │                      │               │
│  │                             │    │  Auth:               │               │
│  │ • db.py                     │───►│  • Token-based       │               │
│  │   - create_user()           │    │  • SHA-256 hashing   │               │
│  │   - verify_user()           │    │  • 7-day sessions    │               │
│  │   - add/remove favorites()  │    │                      │               │
│  │                             │    └──────────────────────┘               │
│  └─────────────────────────────┘                                            │
│                                                                               │
│  ┌───────────────────────────────────────────────────────────────────┐      │
│  │                        CONFIG & MODELS                             │      │
│  ├───────────────────────────────────────────────────────────────────┤      │
│  │                                                                     │      │
│  │  • settings.py - Environment variables & API configuration         │      │
│  │  • schemas.py  - Pydantic models for request/response validation  │      │
│  │                                                                     │      │
│  └───────────────────────────────────────────────────────────────────┘      │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
                    │                              │
                    │                              │
                    ▼                              ▼
┌─────────────────────────────────┐   ┌────────────────────────────────┐
│   GOOGLE MAPS API               │   │   GOOGLE GEMINI AI API         │
├─────────────────────────────────┤   ├────────────────────────────────┤
│                                 │   │                                │
│  • Places API (Text Search)     │   │  • gemini-pro model            │
│  • Place Details API            │   │  • Filters chain businesses    │
│  • Returns nearby businesses    │   │  • Returns small/local only    │
│                                 │   │                                │
└─────────────────────────────────┘   └────────────────────────────────┘
```

## Data Flow

### 1. Search Flow
```
User enters search query + filters
         │
         ▼
    SearchBar.js
         │
         ▼
    App.js (handleSearch)
         │
         ▼
    POST /api/search
         │
         ▼
    search.py route
         │
         ├──► google_maps_service.search_places()
         │              │
         │              ▼
         │         Google Maps API
         │              │
         │              ▼
         │         Returns places
         │
         ├──► gemini_service.filter_small_businesses()
         │              │
         │              ▼
         │         Google Gemini AI
         │              │
         │              ▼
         │         Filters out chains
         │
         ▼
    Returns filtered results
         │
         ▼
    App.js applies client-side filters
         │
         ▼
    BusinessList displays results
```

### 2. Authentication Flow
```
User enters credentials
         │
         ▼
    Auth.js (login/register form)
         │
         ▼
    AuthContext.login() or .register()
         │
         ▼
    POST /api/auth/login or /register
         │
         ▼
    auth.py route
         │
         ▼
    db.py (verify_user or create_user)
         │
         ▼
    SQLite database
         │
         ▼
    Returns token + user data
         │
         ▼
    AuthContext stores token in localStorage
         │
         ▼
    Token sent in Authorization header for future requests
```

### 3. Favorites Flow
```
User clicks favorite star
         │
         ▼
    BusinessList.handleFavoriteToggle()
         │
         ▼
    AuthContext.addFavorite() or .removeFavorite()
         │
         ▼
    POST /api/auth/favorites or DELETE /api/auth/favorites/{id}
         │
         ▼
    auth.py route (verifies token)
         │
         ▼
    db.py (add_favorite or remove_favorite)
         │
         ▼
    SQLite database (favorites table)
         │
         ▼
    Returns success/failure
         │
         ▼
    BusinessList updates favorite state
```

## Technology Stack

### Frontend
- **Framework**: React 18.2.0
- **HTTP Client**: Axios 1.6.2
- **Maps**: @googlemaps/js-api-loader 1.16.2
- **State Management**: React Context API
- **Styling**: CSS3 (responsive design)

### Backend
- **Framework**: FastAPI 0.104.1
- **Server**: Uvicorn 0.24.0 (ASGI)
- **Database**: SQLite3
- **HTTP Client**: httpx 0.25.2 (async)
- **Validation**: Pydantic 2.5.2
- **Environment**: python-dotenv 1.0.0

### External APIs
- **Google Maps Places API**: Text Search, Place Details
- **Google Gemini AI**: gemini-pro model for business filtering

## Security Features

1. **Password Hashing**: SHA-256 for user passwords
2. **Session Management**: Token-based auth with 7-day expiry
3. **CORS**: Configured for http://localhost:3000
4. **API Key Protection**: Stored in .env files (not in git)
5. **Input Validation**: Pydantic schemas validate all requests

## Key Features

### User Features
- ✅ Geolocation detection
- ✅ Search with multiple filters
- ✅ Interactive map with markers
- ✅ User authentication
- ✅ Favorites management
- ✅ Business sharing

### Business Logic
- ✅ AI-powered filtering for small businesses
- ✅ Excludes chain/franchise businesses
- ✅ Real-time search results
- ✅ Distance-based filtering
- ✅ Rating-based filtering
- ✅ Open/closed status filtering

## Deployment Architecture

```
Development:
├── Frontend: http://localhost:3000 (npm start)
└── Backend:  http://localhost:8000 (uvicorn main:app --reload)

Production Ready:
├── Frontend: Static build (npm run build) → Deploy to Vercel/Netlify
├── Backend:  FastAPI app → Deploy to Railway/Render/AWS
└── Database: SQLite → Migrate to PostgreSQL for production
```

## Project Structure

```
ElleHacks/
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── context/         # Global state (Auth)
│   │   ├── App.js          # Main app component
│   │   └── index.js        # Entry point
│   ├── .env.local          # Frontend API keys
│   └── package.json
│
├── backend/
│   ├── api/
│   │   └── routes/         # API endpoints
│   ├── services/           # Business logic
│   ├── database/           # SQLite & ORM
│   ├── models/             # Pydantic schemas
│   ├── config/             # Settings & env
│   ├── .env                # Backend API keys
│   ├── main.py             # FastAPI app
│   └── requirements.txt
│
└── README.md
```
