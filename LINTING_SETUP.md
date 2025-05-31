# 🏒 NHL Prospects App - Code Quality & Linting Setup

This document describes the comprehensive code quality and linting setup for the NHL Prospects App, covering both Python backend and React frontend code.

## 📋 Overview

The project now includes:

- **Python**: Black (formatting), isort (import sorting), flake8 (linting), mypy (type checking)
- **JavaScript/React**: ESLint (linting), Prettier (formatting) with **2-space indentation**
- **Editor Integration**: VS Code/Cursor settings, EditorConfig for universal editor support
- **Automation**: Scripts for running all checks and auto-fixing issues
- **Git Integration**: Pre-commit hooks (optional)

## 🎯 Indentation Standards

- **JavaScript/React/TypeScript**: **2 spaces** (enforced by Prettier + ESLint)
- **Python**: **4 spaces** (enforced by Black + flake8, follows PEP 8)
- **JSON/CSS/HTML**: **2 spaces** (enforced by Prettier)
- **YAML/Shell scripts**: **2 spaces** (enforced by EditorConfig)

## 🐍 Python Tools

### Black (Code Formatter)

- **Purpose**: Automatically formats Python code to a consistent style
- **Config**: `pyproject.toml` - line length 88, Python 3.9 target, **4 spaces**
- **Usage**: `black *.py` or `./fix-python.sh`

### isort (Import Sorter)

- **Purpose**: Sorts and organizes Python imports
- **Config**: `pyproject.toml` - compatible with Black formatting
- **Usage**: `isort *.py` or `./fix-python.sh`

### flake8 (Linter)

- **Purpose**: Checks for Python code style and potential errors
- **Config**: `.flake8` - max line length 88, ignores conflicts with Black
- **Usage**: `flake8 *.py`

### mypy (Type Checker)

- **Purpose**: Static type checking for Python
- **Config**: `pyproject.toml` - moderate strictness, ignores missing imports for third-party packages
- **Usage**: `mypy *.py`

## 🌐 JavaScript/React Tools

### ESLint (Linter)

- **Purpose**: Identifies and fixes JavaScript/React code issues
- **Config**: `app/.eslintrc.js` - React-specific rules, Prettier integration, **2-space indentation rules**, **double quote enforcement**
- **Usage**: `cd app && npm run lint` or `npm run lint:fix`

### Prettier (Code Formatter)

- **Purpose**: Automatically formats JavaScript/React code with **2-space indentation**
- **Config**: `app/.prettierrc` - **double quotes**, semicolons, 80 char width, **tabWidth: 2**
- **Usage**: `cd app && npm run format` or `npm run format:check`

## 🔧 Editor Integration

### VS Code/Cursor Settings

- **File**: `.vscode/settings.json`
- **Features**:
  - Enforces **2-space indentation** for JavaScript/React/TypeScript/JSON/CSS/HTML
  - Enforces **4-space indentation** for Python
  - Format on save enabled
  - ESLint auto-fix on save
  - Prettier as default formatter for web technologies

### EditorConfig

- **File**: `.editorconfig`
- **Features**: Universal editor support for indentation standards
- **Coverage**: All major file types with appropriate indentation settings
- **Compatibility**: Works with VS Code, IntelliJ, Sublime Text, Vim, Emacs, and more

## 🚀 Quick Commands

### Run All Checks

```bash
./lint.sh
```

This comprehensive script runs all linting tools for both Python and JavaScript/React code.

### Auto-Fix Issues

```bash
# Python auto-fix (4 spaces)
./fix-python.sh

# JavaScript/React auto-fix (2 spaces)
cd app && npm run lint:fix && npm run format
```

### Individual Tool Commands

```bash
# Python (4 spaces)
black *.py                    # Format Python code
isort *.py                    # Sort Python imports
flake8 *.py                   # Lint Python code
mypy *.py                     # Type check Python code

# JavaScript/React (2 spaces)
cd app
npm run lint                  # Lint JS/React code
npm run lint:fix              # Auto-fix JS/React issues
npm run format                # Format JS/React code
npm run format:check          # Check JS/React formatting
```

## 📁 Configuration Files

### Python Configuration (4 spaces)

- `pyproject.toml` - Black, isort, and mypy configuration
- `.flake8` - flake8 linting rules and exclusions

### JavaScript/React Configuration (2 spaces)

- `app/.eslintrc.js` - ESLint rules with 2-space indentation enforcement
- `app/.prettierrc` - Prettier formatting with `tabWidth: 2`
- `app/.eslintignore` - Files/directories to exclude from ESLint
- `app/.prettierignore` - Files/directories to exclude from Prettier

### Editor Configuration

- `.vscode/settings.json` - VS Code/Cursor workspace settings
- `.editorconfig` - Universal editor configuration for indentation standards

### Project Configuration

- `.gitignore` - Updated to exclude linting cache files
- `lint.sh` - Comprehensive linting script
- `fix-python.sh` - Python auto-fix script
- `setup-pre-commit.sh` - Pre-commit hooks setup (optional)

## 🔧 Current Status

### ✅ Working Well

- **Black formatting**: All Python files properly formatted with **4 spaces**
- **isort import sorting**: All Python imports properly organized
- **Prettier formatting**: All JavaScript/React files properly formatted with **2 spaces**
- **ESLint**: JavaScript/React code passes with only minor warnings
- **Editor integration**: VS Code/Cursor and EditorConfig ensure consistent indentation

### ⚠️ Minor Issues Remaining

- **flake8**: Some style warnings (E712 comparisons, complexity warnings, unused variables)
- **mypy**: Type annotation warnings and missing type stubs
- **ESLint**: 3 minor warnings (accessibility, equality operators)

### 🎯 Benefits Achieved

- **Consistent indentation standards**: 2 spaces for web tech, 4 spaces for Python
- **Universal editor support**: Works in any editor that supports EditorConfig
- **Automated formatting** eliminates style debates
- **Early error detection** through linting
- **Improved code quality** and maintainability
- **Easy integration** with development workflow

## 🔄 Pre-commit Hooks (Optional)

To automatically run linting before each commit:

```bash
./setup-pre-commit.sh
```

This will:

- Install pre-commit if not already installed
- Set up hooks for Black, isort, flake8, ESLint, and Prettier
- Run checks automatically before each commit
- Prevent commits with linting errors

## 📊 Integration with Development Workflow

### During Development

1. Write code normally (editor will auto-format on save)
2. Run `./lint.sh` periodically to check for issues
3. Use `./fix-python.sh` and `cd app && npm run format` to auto-fix formatting
4. Address any remaining linting warnings manually

### Before Committing

1. Run `./lint.sh` to ensure code quality
2. Fix any critical issues (errors)
3. Consider addressing warnings for better code quality
4. Commit with confidence knowing code follows project standards

### CI/CD Integration

The linting scripts can be easily integrated into CI/CD pipelines:

- Add `./lint.sh` to your CI pipeline
- Fail builds on linting errors
- Generate reports on code quality metrics

## 🛠️ Customization

All linting rules can be customized by editing the respective configuration files:

- Adjust Python line length in `pyproject.toml`
- Modify JavaScript formatting in `app/.prettierrc` (including `tabWidth`)
- Add/remove linting rules in `.flake8` and `app/.eslintrc.js`
- Update indentation settings in `.editorconfig` and `.vscode/settings.json`
- Update file exclusions in ignore files

## 📚 Additional Resources

- [Black Documentation](https://black.readthedocs.io/)
- [isort Documentation](https://pycqa.github.io/isort/)
- [flake8 Documentation](https://flake8.pycqa.org/)
- [mypy Documentation](https://mypy.readthedocs.io/)
- [ESLint Documentation](https://eslint.org/)
- [Prettier Documentation](https://prettier.io/)
- [EditorConfig Documentation](https://editorconfig.org/)
- [VS Code Settings Reference](https://code.visualstudio.com/docs/getstarted/settings)
