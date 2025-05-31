#!/usr/bin/env python3

import requests
from queryParser import convert_api_response_to_old_format, NHL_TEAMS
import predicates

def test_goalie_search():
    """Test goalie search across multiple teams"""
    print("Testing goalie search across multiple teams...")
    
    all_goalies = []
    teams_checked = 0
    
    # Check first 5 teams only for speed
    for team_abbrev in NHL_TEAMS[:5]:
        teams_checked += 1
        print(f"Checking team {team_abbrev}...")
        
        try:
            response = requests.get(f"https://api-web.nhle.com/v1/prospects/{team_abbrev}")
            if response.status_code == 200:
                team_data = response.json()
                
                if 'goalies' in team_data and team_data['goalies']:
                    print(f"  Found {len(team_data['goalies'])} goalies")
                    for player in team_data['goalies']:
                        converted = convert_api_response_to_old_format(player)
                        all_goalies.append((team_abbrev, converted))
                else:
                    print(f"  No goalies")
            else:
                print(f"  API call failed: {response.status_code}")
        except Exception as e:
            print(f"  Error: {e}")
    
    print(f"\nTotal goalies found from {teams_checked} teams: {len(all_goalies)}")
    
    # Test filtering
    filtered_goalies = []
    usePositionFilter = True
    positionFilter = ['G']
    
    for team, p in all_goalies:
        if predicates.filterFour(usePositionFilter, positionFilter, p):
            filtered_goalies.append((team, p))
    
    print(f"Goalies passing position filter: {len(filtered_goalies)}")
    
    for team, goalie in filtered_goalies:
        print(f"  {team}: {goalie['fullName']} (pos: {goalie['primaryPosition']['abbreviation']})")

if __name__ == "__main__":
    test_goalie_search() 