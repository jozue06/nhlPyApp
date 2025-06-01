#!/bin/bash

# NHL Prospects App - Pre-commit Hook Setup
echo "🏒 Setting up pre-commit hooks for NHL Prospects App..."

# Change to project root directory
cd "$(dirname "$0")/.."

# Install pre-commit if not already installed
if ! command -v pre-commit &> /dev/null; then
    echo "Installing pre-commit..."
    pip install pre-commit
fi

# Create pre-commit config
cat > .pre-commit-config.yaml << EOF
repos:
  # Python hooks (backend folder)
  - repo: https://github.com/psf/black
    rev: 25.1.0
    hooks:
      - id: black
        language_version: python3.11
        files: ^backend/.*\.py$

  - repo: https://github.com/pycqa/isort
    rev: 6.0.1
    hooks:
      - id: isort
        args: ["--profile", "black"]
        files: ^backend/.*\.py$

  - repo: https://github.com/pycqa/flake8
    rev: 7.2.0
    hooks:
      - id: flake8
        additional_dependencies: [flake8-docstrings]
        files: ^backend/.*\.py$

  # TypeScript/React hooks (frontend folder)
  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.57.1
    hooks:
      - id: eslint
        files: ^frontend/src/.*\.(ts|tsx)$
        additional_dependencies:
          - eslint@8.57.0
          - eslint-config-prettier
          - eslint-plugin-prettier
          - eslint-plugin-react
          - eslint-plugin-react-hooks
          - prettier
          - typescript

  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.2.5
    hooks:
      - id: prettier
        files: ^frontend/src/.*\.(ts|tsx|css)$

  # General hooks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
EOF

# Install pre-commit hooks
echo "Installing pre-commit hooks..."
pre-commit install

echo "✅ Pre-commit hooks setup completed!"
echo ""
echo "Now all commits will automatically run linting checks."
echo "To run manually: pre-commit run --all-files"
