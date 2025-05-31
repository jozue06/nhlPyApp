#!/bin/bash

# NHL Prospects App - Development Startup Script
# This script starts both the Python Flask backend and React frontend

set -e  # Exit on error

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
if [ ! -f "app.py" ] || [ ! -f "queryParser.py" ]; then
    echo -e "${RED}❌ Error: This script must be run from the nhlPyApp directory${NC}"
    echo -e "${RED}   Make sure you're in the directory containing app.py and queryParser.py${NC}"
    exit 1
fi

# Check if React app directory exists
if [ ! -d "app" ]; then
    echo -e "${RED}❌ Error: React app directory 'app' not found${NC}"
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

# Update React app to use the correct API endpoint
echo -e "${BLUE}📝 Configuring React app API endpoint...${NC}"
cd app/src

# Create or update the API configuration
cat > apiConfig.js << EOF
// Auto-generated API configuration
export const API_BASE_URL = '${API_URL}';
EOF

cd ../..

# Update Form.js to use the configuration
if ! grep -q "apiConfig" app/src/Form.js; then
    echo -e "${BLUE}🔧 Updating Form.js to use dynamic API configuration...${NC}"
    # Create a backup
    cp app/src/Form.js app/src/Form.js.backup
    
    # Update the axios call to use the config
    sed -i.tmp '1i\
import { API_BASE_URL } from "./apiConfig";
' app/src/Form.js
    
    sed -i.tmp 's|http://127.0.0.1:5000|${API_BASE_URL}|g' app/src/Form.js
    
    # Replace the literal string with template literal
    sed -i.tmp 's|"${API_BASE_URL}/api/json/search"|`${API_BASE_URL}/api/json/search`|g' app/src/Form.js
    
    # Clean up temp file
    rm -f app/src/Form.js.tmp
fi

echo ""

# Start Python Flask server (only if running locally)
if [ "$API_MODE" = "local" ]; then
    echo -e "${GREEN}🐍 Starting Python Flask server on port ${PYTHON_PORT}...${NC}"
    
    # Check if virtual environment exists and activate it
    if [ -d ".venv" ]; then
        echo -e "${BLUE}📦 Activating Python virtual environment...${NC}"
        source .venv/bin/activate
    else
        echo -e "${YELLOW}⚠️  No virtual environment found. Install dependencies with: pip install -r requirements.txt${NC}"
    fi
    
    # Start Flask server in background
    python app.py &
    FLASK_PID=$!
    
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

# Start React development server
echo -e "${GREEN}⚛️  Starting React development server on port ${REACT_PORT}...${NC}"
cd app

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo -e "${BLUE}📦 Installing React dependencies...${NC}"
    npm install
fi

# Start React server
echo -e "${GREEN}🚀 Starting React app...${NC}"
npm start &
REACT_PID=$!

cd ..

echo ""
echo -e "${GREEN}✅ React server started (PID: ${REACT_PID})${NC}"
echo -e "${GREEN}   React App: http://localhost:${REACT_PORT}${NC}"
echo ""

echo -e "${BLUE}🎯 All servers are running!${NC}"
echo -e "${BLUE}================================${NC}"
if [ "$API_MODE" = "local" ]; then
    echo -e "${GREEN}🐍 Python Backend: http://127.0.0.1:${PYTHON_PORT}${NC}"
    echo -e "${GREEN}🌐 Flask Web App: http://127.0.0.1:${PYTHON_PORT}${NC}"
fi
echo -e "${GREEN}⚛️  React Dev App: http://localhost:${REACT_PORT}${NC}"
echo ""
echo -e "${YELLOW}💡 Use Ctrl+C to stop all servers${NC}"
echo -e "${YELLOW}💡 To use remote API: ./start-dev.sh remote${NC}"
echo -e "${YELLOW}💡 To use local API: ./start-dev.sh local (or just ./start-dev.sh)${NC}"
echo ""

# Wait for all background processes
wait 