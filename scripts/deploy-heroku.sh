#!/bin/bash

# NHL Prospects App - Heroku Deployment Script
# This script deploys the Python/Flask backend to Heroku with automatic React building

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
echo -e "${BLUE}========================================${NC}"
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

# Python backend uses the bin/post_compile script to build React
echo -e "${BLUE}📝 Using bin/post_compile script for React building${NC}"

# Deploy to Heroku
echo ""
echo -e "${GREEN}🚀 Deploying Python backend to Heroku...${NC}"

# Check if heroku remote exists
if ! git remote | grep -q heroku; then
    echo -e "${RED}❌ Error: Heroku remote not found${NC}"
    echo -e "${RED}   Run: heroku git:remote -a <your-app-name>${NC}"
    exit 1
fi

# Add changes to git
echo -e "${BLUE}📦 Adding deployment files to git...${NC}"
git add .
git commit -m "Deploy Python backend with automatic React building" || echo ""

# Push to Heroku
echo -e "${BLUE}📤 Pushing to Heroku...${NC}"
git push heroku HEAD:main

echo ""
echo -e "${GREEN}🎉 Python backend deployment completed!${NC}"
echo ""
echo -e "${BLUE}🌐 Your app should be available at:${NC}"
heroku_url=$(heroku apps:info --json 2>/dev/null | jq -r '.app.web_url' 2>/dev/null || echo "")
if [ -n "$heroku_url" ] && [ "$heroku_url" != "null" ]; then
    echo -e "${GREEN}   $heroku_url${NC}"
else
    echo -e "${GREEN}   Run 'heroku open' to view your app${NC}"
fi
echo ""
echo -e "${YELLOW}💡 Useful commands:${NC}"
echo -e "${YELLOW}   heroku logs --tail${NC}              # View live logs"
echo -e "${YELLOW}   heroku open${NC}                     # Open app in browser"
echo -e "${YELLOW}   heroku ps${NC}                       # Check dyno status"
echo ""
echo -e "${BLUE}🎯 React frontend built automatically during deployment${NC}"
echo -e "${BLUE}   React app accessible at: /react${NC}"
echo -e "${BLUE}   API endpoints at: /api/json/search${NC}"
echo ""
