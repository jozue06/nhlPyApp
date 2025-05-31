#!/bin/bash

# NHL Prospects App - Python Backend Only
# This script starts just the Python Flask backend server

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🐍 NHL Prospects - Python Backend${NC}"
echo -e "${BLUE}=================================${NC}"

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo -e "${RED}❌ Error: app.py not found. Run this script from the nhlPyApp directory.${NC}"
    exit 1
fi

# Check if virtual environment exists and activate it
if [ -d ".venv" ]; then
    echo -e "${BLUE}📦 Activating Python virtual environment...${NC}"
    source .venv/bin/activate
else
    echo -e "${YELLOW}⚠️  No virtual environment found. Installing dependencies globally...${NC}"
    echo -e "${YELLOW}   Consider creating a virtual environment: python3 -m venv .venv${NC}"
fi

# Install dependencies if needed
if [ -f "requirements.txt" ]; then
    echo -e "${BLUE}📦 Checking Python dependencies...${NC}"
    pip install -r requirements.txt > /dev/null 2>&1
fi

echo -e "${GREEN}🚀 Starting Flask server...${NC}"
echo -e "${GREEN}   Backend API: http://127.0.0.1:5000/api/json/search${NC}"
echo -e "${GREEN}   Web App: http://127.0.0.1:5000${NC}"
echo -e "${GREEN}   React Version: http://127.0.0.1:5000/react${NC}"
echo ""
echo -e "${YELLOW}💡 Use Ctrl+C to stop the server${NC}"
echo ""

# Start Flask server
python app.py 