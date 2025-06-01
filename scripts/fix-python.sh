#!/bin/bash

# NHL Prospects App - Python Auto-Fix Script
echo "🏒 Auto-fixing Python code formatting and imports..."

# Change to project root directory
cd "$(dirname "$0")/.."

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
fi

# Change to backend directory
cd backend

# Python files to format
PYTHON_FILES="*.py"

echo "🔧 Running Black formatter..."
black $PYTHON_FILES

echo ""
echo "🔧 Running isort import sorter..."
isort $PYTHON_FILES

echo ""
echo "✅ Python auto-fix completed!"
echo "Run ./scripts/lint.sh to verify all issues are resolved."
