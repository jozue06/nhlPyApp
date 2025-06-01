#!/bin/bash

# NHL Prospects App - Heroku Deployment Script
# This script deploys either Python/Flask or Go backend to Heroku with automatic React building

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
BACKEND_MODE=${1}  # Backend mode is now required

# Show usage if backend mode is not provided
if [ -z "$BACKEND_MODE" ]; then
    echo -e "${RED}❌ Error: Backend mode is required${NC}"
    echo ""
    echo -e "${YELLOW}Usage: $0 <backend>${NC}"
    echo ""
    echo -e "${BLUE}Backend options:${NC}"
    echo -e "${GREEN}  python${NC}  - Deploy Python Flask backend"
    echo -e "${GREEN}  go${NC}      - Deploy Go backend"
    echo ""
    echo -e "${BLUE}Examples:${NC}"
    echo -e "${YELLOW}  $0 python${NC}  # Deploy Python Flask backend"
    echo -e "${YELLOW}  $0 go${NC}      # Deploy Go backend"
    echo ""
    exit 1
fi

echo -e "${BLUE}🏒 NHL Prospects App - Heroku Deployment (${BACKEND_MODE})${NC}"
echo -e "${BLUE}======================================================${NC}"
echo ""

# Validate backend mode
if [ "$BACKEND_MODE" != "python" ] && [ "$BACKEND_MODE" != "go" ]; then
    echo -e "${RED}❌ Error: Backend mode must be 'python' or 'go'${NC}"
    echo -e "${YELLOW}Usage: $0 [python|go]${NC}"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "backend/app.py" ] || [ ! -d "frontend" ]; then
    echo -e "${RED}❌ Error: This script must be run from the nhlPyApp directory${NC}"
    echo -e "${RED}   Make sure you're in the directory containing backend/ and frontend/${NC}"
    exit 1
fi

# Additional checks for Go backend
if [ "$BACKEND_MODE" = "go" ]; then
    if [ ! -f "backend/go/main.go" ] || [ ! -f "backend/go/go.mod" ]; then
        echo -e "${RED}❌ Error: Go backend files not found (backend/go/main.go, backend/go/go.mod)${NC}"
        echo -e "${RED}   Make sure you're on the golang-backend branch${NC}"
        exit 1
    fi
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

# Clean up any previous deployment files
echo -e "${BLUE}🧹 Cleaning up previous deployment files...${NC}"
rm -f main.go go.mod go.sum *.go 2>/dev/null || true

# Backend-specific preparation
if [ "$BACKEND_MODE" = "go" ]; then
    echo ""
    echo -e "${GREEN}🐹 Preparing Go backend for deployment...${NC}"

    # Copy Go files to root for Heroku deployment
    echo -e "${BLUE}📝 Setting up Go files for Heroku...${NC}"
    cp backend/go/go.mod .
    cp backend/go/*.go .

    # Update file paths in main.go for root deployment
    sed -i.bak 's|../../frontend/build|./frontend/build|g' main.go
    rm -f main.go.bak

    # Create Procfile for Go
    echo "web: ./nhl-app" > Procfile

    # Create .buildpacks file for multi-buildpack support
    cat > .buildpacks << EOF
https://github.com/heroku/heroku-buildpack-nodejs
https://github.com/heroku/heroku-buildpack-go
EOF

    # Create package.json for Node.js buildpack to build React
    cat > package.json << 'EOF'
{
  "name": "nhl-terminal-app",
  "version": "1.0.0",
  "description": "NHL Player Search Terminal App - Go Backend",
  "scripts": {
    "build": "cd frontend && npm install && npm run build",
    "heroku-postbuild": "cd frontend && npm install && npm run build"
  },
  "engines": {
    "node": ">=16.0.0",
    "npm": ">=8.0.0"
  }
}
EOF

    echo -e "${BLUE}📝 Created multi-buildpack configuration for Go backend${NC}"
    echo -e "${GREEN}✅ Go backend preparation completed${NC}"

elif [ "$BACKEND_MODE" = "python" ]; then
    echo ""
    echo -e "${GREEN}🐍 Preparing Python backend for deployment...${NC}"

    # Create Procfile for Python
    echo "web: cd backend && gunicorn app:app --bind 0.0.0.0:\$PORT" > Procfile

    # Python backend uses the existing bin/post_compile script to build React
    echo -e "${BLUE}📝 Using post_compile script for React building${NC}"

    echo -e "${GREEN}✅ Python backend preparation completed${NC}"
fi

# Deploy to Heroku
echo ""
echo -e "${GREEN}🚀 Deploying ${BACKEND_MODE} backend to Heroku...${NC}"

# Check if heroku remote exists
if ! git remote | grep -q heroku; then
    echo -e "${RED}❌ Error: Heroku remote not found${NC}"
    echo -e "${RED}   Run: heroku git:remote -a <your-app-name>${NC}"
    exit 1
fi

# Add changes to git
echo -e "${BLUE}📦 Adding deployment files to git...${NC}"
git add .
git commit -m "Deploy ${BACKEND_MODE} backend - auto-configured for Heroku" || echo "No changes to commit"

# Push to Heroku
echo -e "${BLUE}📤 Pushing to Heroku...${NC}"
git push heroku HEAD:main

echo ""
echo -e "${GREEN}🎉 $(echo ${BACKEND_MODE} | sed 's/./\U&/') backend deployment completed!${NC}"
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
if [ "$BACKEND_MODE" = "go" ]; then
    echo -e "${YELLOW}   heroku config:set GIN_MODE=release${NC}  # Set Go to production mode"
fi
echo ""
echo -e "${BLUE}🎯 Frontend will be automatically built during deployment${NC}"
echo -e "${BLUE}   React app accessible at: /react${NC}"
echo -e "${BLUE}   API endpoints at: /api/json/search${NC}"
echo ""
