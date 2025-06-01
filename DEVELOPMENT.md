# 🛠️ Development Guide

## Quick Start Scripts

### 🚀 **Full Development Environment**

```bash
./start-dev.sh          # Start both Python + React (local API)
./start-dev.sh remote   # Start React only (use remote API)
```

### 🐍 **Python Backend Only**

```bash
./start-backend.sh      # Start Flask server only
```

## Script Features

### **start-dev.sh**

- ✅ Starts Python Flask server (port 5001)
- ✅ Starts React development server (port 3000)
- ✅ Auto-configures API endpoints
- ✅ Installs missing dependencies
- ✅ Graceful shutdown with Ctrl+C
- ✅ Colored terminal output
- ✅ Remote/local API switching

### **start-backend.sh**

- ✅ Starts only Python Flask server
- ✅ Activates virtual environment
- ✅ Installs Python dependencies
- ✅ Simple, focused startup

## Manual Commands

### Python Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run Flask server
python backend/app.py

# Run tests
python3 backend/test_all_filters.py
```

### React Setup

```bash
# Navigate to React app
cd frontend

# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build
```

## URL Reference

### Local Development

- **Python Backend**: http://127.0.0.1:5001
- **Flask Web App**: http://127.0.0.1:5001
- **Flask React**: http://127.0.0.1:5001/react
- **React Dev Server**: http://localhost:3000

### Production/Remote

- **Herokuapp**: https://nhl-terminal.herokuapp.com
- **Remote React**: https://nhl-terminal.herokuapp.com/react

## API Configuration

The React frontend can work with either:

1. **Local Backend**: `http://127.0.0.1:5001` (when running Flask locally)
2. **Remote Backend**: `https://nhl-terminal.herokuapp.com` (production Heroku app)

Configuration is handled by `frontend/src/apiConfig.js` (auto-generated).

## Troubleshooting

### Common Issues

1. **Port 3000 already in use**: Kill existing React processes or use different port
2. **Port 5001 already in use**: Kill existing Flask processes
3. **Missing dependencies**: Run the respective install commands
4. **Permission denied**: Make sure scripts are executable (`chmod +x`)

### Reset Environment

```bash
# Clean React build
cd frontend && rm -rf node_modules build && npm install

# Reset Python environment
pip install -r requirements.txt
```
