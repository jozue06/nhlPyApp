#!/usr/bin/env python3

from queryParser import processIntoHtml

def test_goalies():
    print("Testing goalies query...")
    try:
        result = processIntoHtml('-POS G')
        print(f"Found {len(result)} result lines")
        if result:
            print("All lines:")
            for i, line in enumerate(result):
                print(f"  {i+1}: {repr(line)}")
        else:
            print("No results found")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

def test_limited_goalies():
    print("\nTesting with a simple search (no complex filters)...")
    try:
        # Test one team manually first
        import requests
        from queryParser import convert_api_response_to_old_format, Player
        from processPlayers import processPlayers
        
        response = requests.get("https://api-web.nhle.com/v1/prospects/TOR")
        if response.status_code == 200:
            data = response.json()
            goalies = []
            if 'goalies' in data:
                for player in data['goalies']:
                    converted = convert_api_response_to_old_format(player)
                    goalies.append(Player(p=converted))
            
            print(f"Found {len(goalies)} goalies from TOR")
            
            # Test processPlayers function
            test_results = []
            processPlayers(goalies, test_results)
            print(f"ProcessPlayers generated {len(test_results)} lines")
            for i, line in enumerate(test_results[:10]):
                print(f"  {i+1}: {line}")
                
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

def test_centers():
    print("\nTesting centers query...")
    try:
        result = processIntoHtml('-POS C')
        print(f"Found {len(result)} result lines")
        if result:
            print("First 3 lines:")
            for i, line in enumerate(result[:3]):
                print(f"  {i+1}: {line}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_goalies()
    test_limited_goalies()
    test_centers() 