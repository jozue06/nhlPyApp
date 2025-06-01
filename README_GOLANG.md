# NHL App - Golang Backend

This branch introduces a Golang backend server that replaces the Python/Flask server while maintaining the same API interface for the React frontend.

## Features

- **High-performance Go backend** using Gin framework
- **Full query processing** with the same filter capabilities as the Python version
- **NHL API integration** to fetch real player data
- **React frontend serving** - the Go server can serve the React build
- **CORS enabled** for development and production use

## Query Filters Supported

The Go backend supports all the same query filters as the Python version:

- `-H` or `-h` - Show help menu
- `-CODES "code1,code2"` - Filter by country codes
- `-EXCLUDE-CODES "code1,code2"` - Exclude country codes
- `-HEIGHT 72` / `+HEIGHT 72` - Height filters (in inches)
- `-AGE 25` / `+AGE 25` - Age filters
- `-WEIGHT 200` / `+WEIGHT 200` - Weight filters (in pounds)
- `-POS "C,D"` - Position filter (C, LW, RW, D, G, F for forwards)
- `-HAND L` / `-HAND R` - Handedness filter
- `-RANKED` - Show only ranked players
- `-MAX-RANK 50` / `-MIN-RANK 10` - Rank range filters
- `-ELIG` - Show only draft eligible players

## Setup and Installation

### Prerequisites

- Go 1.21 or later
- Node.js (for building the React frontend)

### Installation

1. **Install Go dependencies:**

   ```bash
   cd backend/go
   go mod download
   cd ../..
   ```

2. **Build the React frontend:**
   ```bash
   cd frontend
   npm install
   npm run build
   cd ..
   ```

## Development

### Running in Development Mode

**⚠️ Important: Backend mode is now required!**

```bash
# Start with Python Flask backend
./scripts/start-dev.sh python

# Start with Go backend
./scripts/start-dev.sh go

# Start with remote API (optional second argument)
./scripts/start-dev.sh python remote
./scripts/start-dev.sh go remote
```

### Manual Development Setup

If you prefer to start servers manually:

1. **Start the Go backend:**

   ```bash
   cd backend/go
   go run .
   ```

2. **In another terminal, start the React dev server:**
   ```bash
   cd frontend
   npm run dev
   ```

### Environment Variables

- `PORT` - Server port (default: 8080 for Go, 5000 for Python)
- `GIN_MODE` - Gin mode (release/debug)
- `VITE_USE_GO_BACKEND` - Set automatically by development script

## API Endpoints

- `POST /api/json/search` - Search for players with query filters
- `GET /` - Serve React application
- `GET /react` - Serve React application
- `GET /assets/*` - Serve React static assets

## Mock Data vs Real API

Currently, the Go backend uses mock data for demonstration. To enable real NHL API data:

1. Replace `getMockPlayers()` call with `fetchAllPlayers()` in `backend/go/main.go`
2. The `fetchAllPlayers()` function is already implemented in `nhl_api.go`

## Architecture

```
Frontend (React/TypeScript)
     ↓ HTTP/JSON
Backend (Go/Gin or Python/Flask)
     ↓ HTTP/JSON
NHL API (api-web.nhle.com)
```

## Deployment

### Heroku Deployment

**⚠️ Important: Backend mode is now required!**

```bash
# Deploy Python Flask backend
./scripts/deploy-heroku.sh python

# Deploy Go backend
./scripts/deploy-heroku.sh go
```

### Manual Deployment

For manual deployment:

**Go Backend:**

```bash
go build -o nhl-app backend/go/*.go
PORT=8080 ./nhl-app
```

**Python Backend:**

```bash
cd backend && python app.py
```

### Production Environment Variables

- `GIN_MODE=release` (for Go backend)
- `PORT` - Set by hosting platform
- Frontend automatically detects production mode

## Performance Benefits

- **Faster response times** due to Go's performance characteristics
- **Lower memory usage** compared to Python
- **Built-in concurrency** for handling multiple API requests
- **Single binary deployment** - no need for virtual environments

## Testing Queries

Once the server is running, you can test queries like:

```bash
# Test defensemen filter
curl -X POST http://localhost:8080/api/json/search \
  -H "Content-Type: application/json" \
  -d '{"queryString": "-POS D"}'

# Test Canadian players
curl -X POST http://localhost:8080/api/json/search \
  -H "Content-Type: application/json" \
  -d '{"queryString": "-CODES CAN"}'

# Test help menu
curl -X POST http://localhost:8080/api/json/search \
  -H "Content-Type: application/json" \
  -d '{"queryString": "-H"}'
```

## Switching Between Backends

The development script automatically configures the frontend to connect to the correct backend:

- **Python mode**: Frontend connects to `http://localhost:5000`
- **Go mode**: Frontend connects to `http://localhost:8080`

No manual configuration needed!
