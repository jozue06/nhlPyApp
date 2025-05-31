# NHL Prospects Filter Test Suite

This directory contains comprehensive tests for all the filter options available in the NHL Prospects application.

## Test Files

### `test_all_filters.py` - Complete Test Suite
Comprehensive test suite that covers all filter options mentioned in the help menu:

**Filter Categories Tested:**
- **Position Filters**: `-POS G/C/L/R/D/F`
- **Draft Filters**: `-RANKED`, `-ELIG`
- **Country Filters**: `-CODES "USA"`, `-CODES "CAN,USA"`
- **Physical Filters**: `-HEIGHT`, `+HEIGHT`, `-WEIGHT`, `+WEIGHT`, `-AGE`, `+AGE`
- **Hand Filters**: `-HAND L/R`
- **Rank Filters**: `-MAX-RANK`, `-MIN-RANK` (limited functionality with new API)
- **Team/League Filters**: `-TEAMS`, `-LEAGUES` (limited functionality with new API)
- **ID Lookup**: `-ID "player_id"`
- **Combined Filters**: Multiple filters in one query
- **Help Menu**: `-H`

**Run the full test suite:**
```bash
python3 test_all_filters.py
```

### `quick_test_demo.py` - Quick Demo
Runs the most important filter tests to demonstrate functionality without taking too long.

**Run the quick demo:**
```bash
python3 quick_test_demo.py
```

## Individual Test Files (Previous)
- `test_prospects.py` - Basic functionality tests
- `debug_prospects.py` - API response debugging
- `debug_full_search.py` - Multi-team search debugging
- `test_manual_search.py` - Manual search implementation test
- `debug_predicates.py` - Filter predicate debugging

## Test Results Overview

### ✅ Fully Working Filters
- **Position filters** (`-POS G/C/L/R/D/F`) - ✅ Working perfectly
- **Country filters** (`-CODES`) - ✅ Working perfectly  
- **Physical filters** (`-HEIGHT`, `-WEIGHT`, `-AGE`) - ✅ Working perfectly
- **Hand filters** (`-HAND`) - ✅ Working perfectly
- **Individual player lookup** (`-ID`) - ✅ Working perfectly
- **Draft eligibility** (`-ELIG`) - ✅ Working (shows all as eligible)
- **Combined filters** - ✅ Working perfectly

### ⚠️ Limited Functionality
- **Rank filters** (`-RANKED`, `-MAX-RANK`, `-MIN-RANK`) - Shows all players (new API lacks ranking data)
- **Team/League filters** (`-TEAMS`, `-LEAGUES`) - Limited (new API lacks amateur team/league data)

### 🎯 Expected Results
- **Total prospects across all teams**: ~700+ players
- **Goalies**: ~80 players
- **USA players**: ~200+ players
- **Combined filters work**: e.g., "USA Goalies" finds ~15+ players

## API Limitations
The new NHL API (`api-web.nhle.com/v1/prospects/{team}`) doesn't provide:
1. Draft ranking data (`ranks`, `midterm`, `finalrank`)
2. Amateur team information (`amateurTeam`)
3. Amateur league information (`amateurLeague`)

The code handles these gracefully by:
- Showing "not currently ranked" for ranking fields
- Filtering treats all players as "eligible"
- Team/league filters will show 0 results

## Performance Notes
- Full test suite takes 5-10 minutes (fetches from all 32 teams multiple times)
- Quick demo takes 2-3 minutes
- Individual tests are much faster
- API calls are throttled to be respectful to the NHL servers 