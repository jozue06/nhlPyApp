#!/bin/bash

# NHL Prospects App - Development Startup Script
# This script starts both the backend (Python Flask or Go) and React TypeScript frontend with Vite

set -e  # Exit on error

# Change to project root directory
cd "$(dirname "$0")/.."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
PYTHON_PORT=5001
GO_PORT=8080
REACT_PORT=3000
BACKEND_MODE=${1}            # Backend mode is now required
API_MODE=${2:-"local"}       # Default to local, can pass "remote" as second argument

# Show usage if backend mode is not provided
if [ -z "$BACKEND_MODE" ]; then
    echo -e "${RED}❌ Error: Backend mode is required${NC}"
    echo ""
    echo -e "${YELLOW}Usage: $0 <backend> [api_mode]${NC}"
    echo ""
    echo -e "${BLUE}Backend options:${NC}"
    echo -e "${GREEN}  python${NC}  - Start Python Flask backend on port $PYTHON_PORT"
    echo -e "${GREEN}  go${NC}      - Start Go backend on port $GO_PORT"
    echo ""
    echo -e "${BLUE}API mode options (optional):${NC}"
    echo -e "${GREEN}  local${NC}   - Use local backend (default)"
    echo -e "${GREEN}  remote${NC}  - Use remote API (heroku)"
    echo ""
    echo -e "${BLUE}Examples:${NC}"
    echo -e "${YELLOW}  $0 python${NC}        # Start with Python backend"
    echo -e "${YELLOW}  $0 go${NC}            # Start with Go backend"
    echo -e "${YELLOW}  $0 python remote${NC}  # Use Python backend with remote API"
    echo -e "${YELLOW}  $0 go remote${NC}      # Use Go backend with remote API"
    echo ""
    exit 1
fi

echo -e "${BLUE}🏒 NHL Prospects App - Development Startup${NC}"
echo -e "${BLUE}=============================================${NC}"
echo ""

# Clean up any existing servers on the ports we'll use
echo -e "${YELLOW}🧹 Cleaning up existing servers...${NC}"
lsof -ti:3000 | xargs kill -9 2>/dev/null; lsof -ti:5000 | xargs kill -9 2>/dev/null; lsof -ti:5001 | xargs kill -9 2>/dev/null; lsof -ti:8080 | xargs kill -9 2>/dev/null; echo "Killed all servers on ports 3000, 5000, 5001, and 8080"
echo ""

# Function to cleanup background processes on exit
cleanup() {
    echo -e "\n${YELLOW}⏹️  Shutting down servers...${NC}"
    # Kill all background jobs started by this script
    jobs -p | xargs -r kill
    exit
}

# Set up cleanup trap
trap cleanup SIGINT SIGTERM EXIT

# Validate backend mode
if [ "$BACKEND_MODE" != "python" ] && [ "$BACKEND_MODE" != "go" ]; then
    echo -e "${RED}❌ Error: Backend mode must be 'python' or 'go'${NC}"
    echo -e "${YELLOW}Usage: $0 [python|go] [local|remote]${NC}"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "backend/app.py" ] || [ ! -f "backend/queryParser.py" ]; then
    echo -e "${RED}❌ Error: This script must be run from the nhlPyApp directory${NC}"
    echo -e "${RED}   Make sure you're in the directory containing backend/app.py and backend/queryParser.py${NC}"
    exit 1
fi

# Check if React frontend directory exists
if [ ! -d "frontend" ]; then
    echo -e "${RED}❌ Error: React frontend directory 'frontend' not found${NC}"
    exit 1
fi

# Set backend port and check for Go files if using Go mode
if [ "$BACKEND_MODE" = "go" ]; then
    BACKEND_PORT=$GO_PORT
    if [ ! -f "backend/go/main.go" ] || [ ! -f "backend/go/go.mod" ]; then
        echo -e "${RED}❌ Error: Go backend files not found (backend/go/main.go, backend/go/go.mod)${NC}"
        echo -e "${RED}   Make sure you're on the golang-backend branch${NC}"
        exit 1
    fi
else
    BACKEND_PORT=$PYTHON_PORT
fi

# Configure API endpoint based on mode
if [ "$API_MODE" = "remote" ]; then
    API_URL="https://nhl-terminal.herokuapp.com"
    echo -e "${YELLOW}🌐 API Mode: Remote (${API_URL})${NC}"
else
    API_URL="http://127.0.0.1:${BACKEND_PORT}"
    echo -e "${YELLOW}🏠 API Mode: Local ${BACKEND_MODE} backend (${API_URL})${NC}"
fi

# Update React frontend to use the correct API endpoint and backend mode
echo -e "${BLUE}📝 Configuring React TypeScript frontend API endpoint...${NC}"
cd frontend/src

# Create the environment variable for Vite
if [ "$BACKEND_MODE" = "go" ]; then
    echo "VITE_USE_GO_BACKEND=true" > ../.env.development
else
    echo "VITE_USE_GO_BACKEND=false" > ../.env.development
fi

cd ../..

echo ""

# Build React app for production (needed for backends to serve static files)
echo -e "${BLUE}⚛️  Building React TypeScript app for production...${NC}"
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo -e "${BLUE}📦 Installing React TypeScript dependencies...${NC}"
    npm install
fi

# Build the React app
echo -e "${GREEN}🏗️  Building React app...${NC}"
npm run build

cd ..

echo ""

# Start backend server (only if running locally)
if [ "$API_MODE" = "local" ]; then
    if [ "$BACKEND_MODE" = "go" ]; then
        echo -e "${GREEN}🐹 Starting Go backend server on port ${GO_PORT}...${NC}"

        # Check if Go is installed
        if ! command -v go &> /dev/null; then
            echo -e "${RED}❌ Error: Go is not installed. Please install Go 1.21 or later${NC}"
            exit 1
        fi

        # Download Go dependencies if needed
        if [ ! -d "backend/go/vendor" ] && [ -f "backend/go/go.mod" ]; then
            echo -e "${BLUE}📦 Downloading Go dependencies...${NC}"
            cd backend/go && go mod download && cd ../..
        fi

        # Start Go server in background
        cd backend/go
        go run . &
        BACKEND_PID=$!
        cd ../../  # Return to project root

        echo -e "${GREEN}✅ Go server started (PID: ${BACKEND_PID})${NC}"
        echo -e "${GREEN}   Backend API: http://127.0.0.1:${GO_PORT}${NC}"
        echo -e "${GREEN}   Web App: http://127.0.0.1:${GO_PORT}${NC}"
        echo -e "${GREEN}   Web React: http://127.0.0.1:${GO_PORT}/react${NC}"
        echo ""

        # Wait a moment for Go server to start
        sleep 3
    else
        echo -e "${GREEN}🐍 Starting Python Flask server on port ${PYTHON_PORT}...${NC}"

        # Check if virtual environment exists and activate it
        if [ -d ".venv" ]; then
            echo -e "${BLUE}📦 Activating Python virtual environment...${NC}"
            source .venv/bin/activate
        else
            echo -e "${YELLOW}⚠️  No virtual environment found. Install dependencies with: pip install -r backend/requirements.txt${NC}"
        fi

        # Start Flask server in background from backend directory
        cd backend
        python app.py &
        BACKEND_PID=$!
        cd ..

        echo -e "${GREEN}✅ Flask server started (PID: ${BACKEND_PID})${NC}"
        echo -e "${GREEN}   Backend API: http://127.0.0.1:${PYTHON_PORT}${NC}"
        echo -e "${GREEN}   Web App: http://127.0.0.1:${PYTHON_PORT}${NC}"
        echo -e "${GREEN}   Web React: http://127.0.0.1:${PYTHON_PORT}/react${NC}"
        echo ""

        # Wait a moment for Flask to start
        sleep 3
    fi
else
    echo -e "${BLUE}🌐 Using remote API at ${API_URL}${NC}"
    echo ""
fi

# Start React development server with Vite
echo -e "${GREEN}⚛️  Starting React TypeScript development server with Vite on port ${REACT_PORT}...${NC}"

# Ensure we're in the project root directory
# If we're in the scripts directory, go up one level
if [[ "$(basename $(pwd))" == "scripts" ]]; then
    cd ..
fi

# If we still don't see frontend, something is wrong
if [ ! -d "frontend" ]; then
    echo -e "${RED}❌ Error: Cannot find frontend directory from $(pwd)${NC}"
    echo -e "${RED}   Current directory contents:${NC}"
    ls -la
    exit 1
fi

cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo -e "${BLUE}📦 Installing React TypeScript dependencies...${NC}"
    npm install
fi

# Start Vite dev server
echo -e "${GREEN}🚀 Starting Vite dev server...${NC}"
npm run dev &
REACT_PID=$!

cd ..

echo ""
echo -e "${GREEN}✅ Vite dev server started (PID: ${REACT_PID})${NC}"
echo -e "${GREEN}   React TypeScript App: http://localhost:${REACT_PORT}${NC}"
echo ""

echo -e "${BLUE}🎯 All servers are running!${NC}"
echo -e "${BLUE}================================${NC}"
if [ "$API_MODE" = "local" ]; then
    if [ "$BACKEND_MODE" = "go" ]; then
        echo -e "${GREEN}🐹 Go Backend: http://127.0.0.1:${GO_PORT}${NC}"
    else
        echo -e "${GREEN}🐍 Python Backend: http://127.0.0.1:${PYTHON_PORT}${NC}"
    fi
    echo -e "${GREEN}🌐 Backend Web App: http://127.0.0.1:${BACKEND_PORT}${NC}"
fi
echo -e "${GREEN}⚛️  React TypeScript + Vite: http://localhost:${REACT_PORT}${NC}"
echo ""
echo -e "${YELLOW}💡 Use Ctrl+C to stop all servers${NC}"
echo -e "${YELLOW}💡 Backend modes:${NC}"
echo -e "${YELLOW}   Python: ./scripts/start-dev.sh python${NC}"
echo -e "${YELLOW}   Go:     ./scripts/start-dev.sh go${NC}"
echo -e "${YELLOW}💡 With remote API: ./scripts/start-dev.sh [python|go] remote${NC}"
echo ""

# Wait for all background processes
wait
