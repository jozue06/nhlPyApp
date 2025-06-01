# 🏒 NHL Prospects Explorer

A comprehensive Python application for exploring NHL prospect data, featuring both terminal-style queries and modern React web interface. The app leverages the official NHL API to provide up-to-date prospect information across all 32 NHL teams.

## 🌟 Features

### 🔍 **Advanced Filtering System**

- **Position Filters**: Search by specific positions (C, L, R, D, G) or all forwards
- **Country Filters**: Filter by birth country using country codes (USA, CAN, SWE, etc.)
- **Country Exclusion**: Exclude specific countries from search results
- **Physical Filters**: Search by height, weight, and age ranges
- **Hand Preference**: Filter by shooting/catching hand (L/R)
- **Rank Filters**: Search by draft rankings (when available)
- **Combined Filters**: Mix and match any filters for precise searches

### 🖥️ **Multiple Interfaces**

1. **Python Terminal**: Direct command-line looking interface for power users
2. **Flask Web App**: Server-rendered HTML interface
3. **React SPA**: Modern single-page application with dynamic UI

## 🚀 Quick Start

### **Option 1: Automated Development Setup (Recommended)**

```bash
# Clone and navigate to the project
git clone <your-repo-url>
cd nhlPyApp

# Run both Python backend + React frontend
./start-dev.sh

# Or use remote API instead of local Python server
./start-dev.sh remote
```

This will automatically:

- ✅ Start Python Flask server on port 5001
- ✅ Start React development server on port 3000
- ✅ Configure API endpoints dynamically
- ✅ Install missing dependencies
- ✅ Provide colored terminal output with helpful URLs

### **Option 2: Manual Setup**

#### Python Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Start Flask server
python backend/app.py
```

#### React Frontend Setup

```bash
# Navigate to React app
cd frontend

# Install Node dependencies
npm install

# Start React development server
npm start
```

## 🎯 Usage Examples

### **Help Menu**

```bash
# Get all available filter options
-H
```

### **Position Searches**

```bash
# All goalies
-POS G

# All centers
-POS C

# All forwards (centers + wings)
-POS F

# All defensemen
-POS D
```

### **Country Searches**

```bash
# USA players only
-CODES "USA"

# Canadian players only
-CODES "CAN"

# Multiple countries
-CODES "USA,CAN,SWE"

# Exclude USA players (show all except USA)
-EXCLUDE-CODES "USA"

# Exclude multiple countries
-EXCLUDE-CODES "USA,CAN"

# Combine include and exclude (European players only)
-CODES "SWE,FIN,RUS" -EXCLUDE-CODES "USA,CAN"
```

### **Physical Attribute Searches**

```bash
# Players 21 and younger
-AGE "21"

# Players 23 and older
+AGE "23"

# Players 6'2" and under
-HEIGHT "6'2""

# Players 6'4" and taller
+HEIGHT "6'4""

# Players 200lbs and under
-WEIGHT "200"

# Left-handed players
-HAND "L"
```

### **Combined Searches**

```bash
# Young USA goalies
-POS G -CODES "USA" -AGE "21"

# Tall Canadian centers
-POS C -CODES "CAN" +HEIGHT "6'2""

# Left-handed defensemen from Sweden
-POS D -CODES "SWE" -HAND "L"

# Non-North American goalies
-POS G -EXCLUDE-CODES "USA,CAN"
```

### **Individual Player Lookup**

```bash
# Find specific player by NHL ID
-ID "8479361"
```

## 🔧 Technical Details

### **Architecture**

- **Backend**: Python 3.11+ with Flask web framework
- **Frontend**: React 17+ with fetch for API calls
- **Data Source**: Official NHL Prospects API (`api-web.nhle.com`)
- **Filtering**: Custom predicate system with boolean logic
- **Sorting**: Multi-criteria sorting with fallback mechanisms

### **API Integration**

- **32 Team Endpoints**: Loops through all NHL team abbreviations
- **Error Handling**: Graceful handling of API failures and missing data
- **Rate Limiting**: Respectful API usage with proper delays

### **Key Files**

- `backend/app.py` - Flask web server and API routes
- `backend/queryParser.py` - Main query processing and API integration
- `backend/predicates.py` - Filter logic and boolean operations
- `backend/sorting.py` - Multi-criteria sorting algorithms
- `backend/utils.py` - Helper functions for data conversion
- `frontend/src/Form.tsx` - React frontend component

## 🌐 Deployment

### **Live Demo**

- **Herokuapp**: [https://nhl-terminal.herokuapp.com](https://nhl-terminal.herokuapp.com)
- **React Version**: [https://nhl-terminal.herokuapp.com/react](https://nhl-terminal.herokuapp.com/react)

### **Local URLs (when running)**

- **Python Backend API**: http://127.0.0.1:5001
- **Flask Web App**: http://127.0.0.1:5001
- **Flask React Served**: http://127.0.0.1:5001/react
- **React Dev Server**: http://localhost:3000

## 🧪 Testing

```bash
# Run comprehensive filter test suite
python3 backend/test_all_filters.py

# Quick demo of key filters
python3 backend/quick_test_demo.py

# Manual testing
python3 -c "from backend.queryParser import processQueryStringJSON; import json; print(json.dumps(processQueryStringJSON('-POS G'), indent=2))"
```

## 📝 Recent Updates

### **✅ API Migration Complete**

- ✅ Migrated from deprecated API to new NHL endpoints
- ✅ Updated data structure handling for multilingual fields
- ✅ Fixed all filter logic bugs and parameter mismatches
- ✅ Comprehensive test suite with 100% pass rate
- ✅ Enhanced error handling and fallback mechanisms

### **🔄 API Limitations**

- **Draft Rankings**: Not available in new API (shows all players)
- **Amateur Teams/Leagues**: Not provided in new API structure
- **Current League Info**: No information about what league players currently play in
- **Height Filtering**: May show limited results due to data format

## 🤝 Contributing

Feel free to submit issues and enhancement requests! The codebase is well-documented and modular for easy extension.

## 📄 License

This project is for educational and personal use, utilizing publicly available NHL API data.

---

_Built with ❤️ for hockey fans and data enthusiasts_
