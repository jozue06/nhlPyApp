#!/bin/bash

# NHL Prospects App - Development Startup Script
# This script starts both the Python Flask backend and React TypeScript frontend with Vite

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
PYTHON_PORT=5000
REACT_PORT=3000
API_MODE=${1:-"local"}  # Default to local, can pass "remote" as first argument

echo -e "${BLUE}🏒 NHL Prospects App - Development Startup${NC}"
echo -e "${BLUE}=============================================${NC}"
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
    echo -e "${YELLOW}🏠 API Mode: Local (${API_URL})${NC}"
fi

# Update React frontend to use the correct API endpoint
echo -e "${BLUE}📝 Configuring React TypeScript frontend API endpoint...${NC}"
cd frontend/src

# Create or update the API configuration for TypeScript
cat > apiConfig.ts << EOF
// Auto-generated API configuration
export const API_BASE_URL: string = '${API_URL}';
EOF

cd ../..

echo ""

# Start Python Flask server (only if running locally)
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
    FLASK_PID=$!
    cd ..

    echo -e "${GREEN}✅ Flask server started (PID: ${FLASK_PID})${NC}"
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

# Start React development server with Vite
echo -e "${GREEN}⚛️  Starting React TypeScript development server with Vite on port ${REACT_PORT}...${NC}"
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
    echo -e "${GREEN}🐍 Python Backend: http://127.0.0.1:${PYTHON_PORT}${NC}"
    echo -e "${GREEN}🌐 Flask Web App: http://127.0.0.1:${PYTHON_PORT}${NC}"
fi
echo -e "${GREEN}⚛️  React TypeScript + Vite: http://localhost:${REACT_PORT}${NC}"
echo ""
echo -e "${YELLOW}💡 Use Ctrl+C to stop all servers${NC}"
echo -e "${YELLOW}💡 To use remote API: ./scripts/start-dev.sh remote${NC}"
echo -e "${YELLOW}💡 To use local API: ./scripts/start-dev.sh local (or just ./scripts/start-dev.sh)${NC}"
echo ""

# Wait for all background processes
wait
