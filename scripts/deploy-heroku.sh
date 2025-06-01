#!/bin/bash

# NHL Prospects App - Heroku Deployment Script
# This script builds the React frontend and deploys the Python/Flask backend to Heroku

set -e  # Exit on error

# Change to project root directory
cd "$(dirname "$0")/.."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🏒 NHL Prospects App - Heroku Deployment${NC}"
echo -e "${BLUE}=========================================${NC}"
echo ""

# Check if we're in the right directory
if [ ! -f "backend/app.py" ] || [ ! -d "frontend" ]; then
    echo -e "${RED}❌ Error: This script must be run from the nhlPyApp directory${NC}"
    echo -e "${RED}   Make sure you're in the directory containing backend/ and frontend/${NC}"
    exit 1
fi

# Check if git is clean
if [ -n "$(git status --porcelain)" ]; then
    echo -e "${YELLOW}⚠️  Warning: You have uncommitted changes${NC}"
    echo -e "${YELLOW}   Consider committing your changes first${NC}"
    echo ""
    git status --short
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Deployment cancelled${NC}"
        exit 1
    fi
fi

# Build React frontend for production
echo -e "${GREEN}⚛️  Building React TypeScript frontend...${NC}"
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo -e "${BLUE}📦 Installing frontend dependencies...${NC}"
    npm install
fi

# Build for production
echo -e "${BLUE}🔨 Building for production...${NC}"
npm run build

# Check if build was successful
if [ ! -d "build" ]; then
    echo -e "${RED}❌ Frontend build failed - build directory not found${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Frontend build completed successfully${NC}"
echo -e "${GREEN}   Build output: frontend/build/${NC}"

# Go back to root directory
cd ..

# Deploy to Heroku
echo ""
echo -e "${GREEN}🚀 Deploying to Heroku...${NC}"

# Check if heroku remote exists
if ! git remote | grep -q heroku; then
    echo -e "${RED}❌ Error: Heroku remote not found${NC}"
    echo -e "${RED}   Run: heroku git:remote -a <your-app-name>${NC}"
    exit 1
fi

# Push to Heroku
echo -e "${BLUE}📤 Pushing to Heroku master...${NC}"
git push heroku master

echo ""
echo -e "${GREEN}🎉 Deployment completed!${NC}"
echo ""
echo -e "${BLUE}🌐 Your app should be available at:${NC}"
echo -e "${GREEN}   https://$(heroku apps:info --json | jq -r '.app.web_url' | sed 's|https://||' | sed 's|/$||').herokuapp.com${NC}"
echo ""
echo -e "${YELLOW}💡 Useful commands:${NC}"
echo -e "${YELLOW}   heroku logs --tail${NC}    # View live logs"
echo -e "${YELLOW}   heroku open${NC}           # Open app in browser"
echo -e "${YELLOW}   heroku ps${NC}             # Check dyno status"
echo ""
