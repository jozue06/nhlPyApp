#!/bin/bash

# NHL Prospects App - Heroku Deployment Script
# This script builds the React frontend and deploys either Python/Flask or Go backend to Heroku

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

# Backend-specific preparation
if [ "$BACKEND_MODE" = "go" ]; then
    echo ""
    echo -e "${GREEN}🐹 Preparing Go backend for deployment...${NC}"

    # For Heroku Go buildpack, copy the Go files to root temporarily
    echo -e "${BLUE}📝 Setting up Go files for Heroku...${NC}"

    # Copy Go files to root for Heroku deployment
    cp backend/go/go.mod .
    cp backend/go/*.go .

    # Update file paths in main.go for root deployment
    sed -i.bak 's|../../frontend/build|frontend/build|g' main.go

    # Create or update Procfile for Go
    echo "web: go run ." > Procfile
    echo -e "${BLUE}📝 Created Procfile for Go backend${NC}"

    # Ensure Go buildpack is set
    echo -e "${BLUE}🔧 Setting up Go buildpack...${NC}"
    heroku buildpacks:clear 2>/dev/null || true
    heroku buildpacks:add heroku/go

    echo -e "${GREEN}✅ Go backend preparation completed${NC}"

elif [ "$BACKEND_MODE" = "python" ]; then
    echo ""
    echo -e "${GREEN}🐍 Preparing Python backend for deployment...${NC}"

    # Clean up any Go files from root if they exist
    rm -f main.go go.mod *.go 2>/dev/null || true

    # Create or update Procfile for Python
    echo "web: cd backend && python app.py" > Procfile
    echo -e "${BLUE}📝 Created Procfile for Python backend${NC}"

    # Ensure Python buildpack is set
    echo -e "${BLUE}🔧 Setting up Python buildpack...${NC}"
    heroku buildpacks:clear 2>/dev/null || true
    heroku buildpacks:add heroku/python

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

# Add changes to git if needed
if [ -n "$(git status --porcelain)" ]; then
    echo -e "${BLUE}📦 Adding deployment files to git...${NC}"
    git add .
    git commit -m "Deploy ${BACKEND_MODE} backend with frontend build" || echo "No changes to commit"
fi

# Push to Heroku
echo -e "${BLUE}📤 Pushing to Heroku master...${NC}"
git push heroku HEAD:master

echo ""
echo -e "${GREEN}🎉 ${BACKEND_MODE^} backend deployment completed!${NC}"
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
echo -e "${YELLOW}   heroku logs --tail${NC}    # View live logs"
echo -e "${YELLOW}   heroku open${NC}           # Open app in browser"
echo -e "${YELLOW}   heroku ps${NC}             # Check dyno status"
if [ "$BACKEND_MODE" = "go" ]; then
    echo -e "${YELLOW}   heroku config:set GIN_MODE=release${NC}  # Set Go to production mode"
fi
echo ""
