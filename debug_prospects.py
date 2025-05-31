#!/usr/bin/env python3

import requests
from queryParser import convert_api_response_to_old_format

def debug_api_response():
    """Debug the API response structure"""
    print("Testing API response for TOR...")
    response = requests.get("https://api-web.nhle.com/v1/prospects/TOR")
    if response.status_code == 200:
        data = response.json()
        print(f"Response keys: {list(data.keys())}")
        
        for position_group in ['forwards', 'defensemen', 'goalies']:
            if position_group in data:
                print(f"\n{position_group}: {len(data[position_group])} players")
                if data[position_group]:
                    # Show first player details
                    player = data[position_group][0]
                    print(f"First {position_group[:-1]} example:")
                    print(f"  Raw data keys: {list(player.keys())}")
                    print(f"  Position code: {player.get('positionCode')}")
                    print(f"  Name: {player.get('firstName', {}).get('default')} {player.get('lastName', {}).get('default')}")
                    
                    # Convert and check
                    converted = convert_api_response_to_old_format(player)
                    print(f"  Converted position: {converted['primaryPosition']}")
    else:
        print(f"API call failed: {response.status_code}")

def test_filtering():
    """Test the filtering logic"""
    from queryParser import NHL_TEAMS
    import predicates
    
    print("\nTesting filtering logic...")
    
    # Get some test data
    response = requests.get("https://api-web.nhle.com/v1/prospects/TOR")
    if response.status_code == 200:
        data = response.json()
        
        all_positions = []
        all_converted = []
        
        for position_group in ['forwards', 'defensemen', 'goalies']:
            if position_group in data:
                for player in data[position_group]:
                    converted = convert_api_response_to_old_format(player)
                    all_converted.append(converted)
                    all_positions.append(converted['primaryPosition']['abbreviation'])
        
        print(f"All positions found: {set(all_positions)}")
        print(f"Total prospects: {len(all_converted)}")
        
        # Test goalie filter
        goalie_filter = ['G']
        goalies_found = []
        
        for p in all_converted:
            if predicates.filterFour(True, goalie_filter, p):
                goalies_found.append(p['fullName'])
        
        print(f"Goalies found with filter: {goalies_found}")

if __name__ == "__main__":
    debug_api_response()
    test_filtering() 