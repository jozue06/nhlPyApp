#!/bin/bash

# NHL Prospects App - Development Startup Script
# This script starts the Python Flask backend and React TypeScript frontend with Vite

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
REACT_PORT=3000
API_MODE=${1:-"local"}       # Default to local, can pass "remote" as first argument

echo -e "${BLUE}🏒 NHL Prospects App - Development Startup${NC}"
echo -e "${BLUE}=============================================${NC}"
echo ""

# Show usage
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    echo -e "${YELLOW}Usage: $0 [api_mode]${NC}"
    echo ""
    echo -e "${BLUE}API mode options (optional):${NC}"
    echo -e "${GREEN}  local${NC}   - Use local Python backend (default)"
    echo -e "${GREEN}  remote${NC}  - Use remote API (heroku)"
    echo ""
    echo -e "${BLUE}Examples:${NC}"
    echo -e "${YELLOW}  $0${NC}            # Start with local Python backend"
    echo -e "${YELLOW}  $0 local${NC}      # Start with local Python backend"
    echo -e "${YELLOW}  $0 remote${NC}     # Use remote API"
    echo ""
    exit 0
fi

# Clean up any existing servers on the ports we'll use
echo -e "${YELLOW}🧹 Cleaning up existing servers...${NC}"
lsof -ti:3000 | xargs kill -9 2>/dev/null; lsof -ti:5001 | xargs kill -9 2>/dev/null; echo "Killed all servers on ports 3000 and 5001"
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

# Validate API mode
if [ "$API_MODE" != "local" ] && [ "$API_MODE" != "remote" ]; then
    echo -e "${RED}❌ Error: API mode must be 'local' or 'remote'${NC}"
    echo -e "${YELLOW}Usage: $0 [local|remote]${NC}"
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

# Configure API endpoint based on mode
if [ "$API_MODE" = "remote" ]; then
    API_URL="https://nhl-terminal.herokuapp.com"
    echo -e "${YELLOW}🌐 API Mode: Remote (${API_URL})${NC}"
else
    API_URL="http://127.0.0.1:${PYTHON_PORT}"
    echo -e "${YELLOW}🏠 API Mode: Local Python backend (${API_URL})${NC}"
fi

# Update React frontend configuration
echo -e "${BLUE}📝 Configuring React TypeScript frontend...${NC}"

echo ""

# Build React app for production (needed for backend to serve static files)
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
else
    echo -e "${BLUE}🌐 Using remote API at ${API_URL}${NC}"
    echo ""
fi

# Start React development server
echo -e "${GREEN}⚛️  Starting React TypeScript development server on port ${REACT_PORT}...${NC}"
cd frontend

# Start Vite dev server in the foreground (last process)
echo -e "${GREEN}🚀 Development servers are starting up...${NC}"
echo ""
if [ "$API_MODE" = "local" ]; then
    echo -e "${BLUE}📊 Available Services:${NC}"
    echo -e "${GREEN}   • Python Backend API: http://127.0.0.1:${PYTHON_PORT}/api/json/search${NC}"
    echo -e "${GREEN}   • Python React App: http://127.0.0.1:${PYTHON_PORT}/react${NC}"
    echo -e "${GREEN}   • React Dev Server: http://127.0.0.1:${REACT_PORT}${NC}"
else
    echo -e "${BLUE}📊 Available Services:${NC}"
    echo -e "${GREEN}   • Remote API: ${API_URL}${NC}"
    echo -e "${GREEN}   • React Dev Server: http://127.0.0.1:${REACT_PORT}${NC}"
fi
echo ""
echo -e "${YELLOW}💡 Press Ctrl+C to stop all servers${NC}"
echo ""

# This runs in the foreground and will be the main process
npm run dev
