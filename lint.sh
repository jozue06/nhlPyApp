#!/bin/bash

# NHL Prospects App - Comprehensive Linting Script
echo "🏒 NHL Prospects App - Running Code Quality Checks 🏒"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" == "" ]]; then
    print_warning "Not in a virtual environment. Activating .venv..."
    source .venv/bin/activate
fi

# Python files to lint (excluding certain directories)
PYTHON_FILES="*.py"

echo ""
print_status "🐍 Running Python Code Quality Checks..."
echo "----------------------------------------"

# 1. Black formatting check
print_status "Running Black (Python formatter)..."
if black --check --diff $PYTHON_FILES; then
    print_success "Black formatting: PASSED"
else
    print_error "Black formatting: FAILED"
    echo "Run 'black $PYTHON_FILES' to fix formatting issues"
fi

echo ""

# 2. isort import sorting check
print_status "Running isort (import sorter)..."
if isort --check-only --diff $PYTHON_FILES; then
    print_success "isort import sorting: PASSED"
else
    print_error "isort import sorting: FAILED"
    echo "Run 'isort $PYTHON_FILES' to fix import sorting"
fi

echo ""

# 3. flake8 linting
print_status "Running flake8 (Python linter)..."
if flake8 $PYTHON_FILES; then
    print_success "flake8 linting: PASSED"
else
    print_error "flake8 linting: FAILED"
fi

echo ""

# 4. mypy type checking
print_status "Running mypy (type checker)..."
if mypy $PYTHON_FILES; then
    print_success "mypy type checking: PASSED"
else
    print_warning "mypy type checking: WARNINGS (some issues found)"
fi

echo ""
print_status "🌐 Running JavaScript/React Code Quality Checks..."
echo "------------------------------------------------"

# Change to React app directory
cd app

# 5. ESLint for React/JS
print_status "Running ESLint (JavaScript/React linter)..."
if npm run lint; then
    print_success "ESLint: PASSED"
else
    print_error "ESLint: FAILED"
    echo "Run 'npm run lint:fix' to auto-fix some issues"
fi

echo ""

# 6. Prettier formatting check
print_status "Running Prettier (JavaScript/React formatter)..."
if npm run format:check; then
    print_success "Prettier formatting: PASSED"
else
    print_error "Prettier formatting: FAILED"
    echo "Run 'npm run format' to fix formatting issues"
fi

# Go back to root directory
cd ..

echo ""
echo "=================================================="
print_status "✅ Code quality checks completed!"
echo ""
print_status "🔧 To fix issues automatically:"
echo "   Python: ./fix-python.sh"
echo "   React:  cd app && npm run lint:fix && npm run format"
echo "" 