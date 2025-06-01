#!/usr/bin/env python3

from queryParser import processQueryStringJSON


def test_goalies():
    print("Testing goalies query...")
    try:
        result = processQueryStringJSON("-POS G")
        players = result.get("players", [])
        print(f"Found {len(players)} goalies")
        if players:
            print("First 5 goalies:")
            for i, player in enumerate(players[:5]):
                print(f"  {i+1}: {player.get('fullName')} - {player.get('primaryPosition', {}).get('abbreviation')}")
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
        from queryParser import create_player_from_api_data

        response = requests.get("https://api-web.nhle.com/v1/prospects/TOR")
        if response.status_code == 200:
            data = response.json()
            goalies = []
            if "goalies" in data:
                for player in data["goalies"]:
                    converted = create_player_from_api_data(player)
                    goalies.append(converted)

            print(f"Found {len(goalies)} goalies from TOR")
            for i, goalie in enumerate(goalies[:5]):
                print(f"  {i+1}: {goalie.get('fullName')} - {goalie.get('primaryPosition', {}).get('abbreviation')}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


def test_centers():
    print("\nTesting centers query...")
    try:
        result = processQueryStringJSON("-POS C")
        players = result.get("players", [])
        print(f"Found {len(players)} centers")
        if players:
            print("First 3 centers:")
            for i, player in enumerate(players[:3]):
                print(f"  {i+1}: {player.get('fullName')} - {player.get('primaryPosition', {}).get('abbreviation')}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    test_goalies()
    test_limited_goalies()
    test_centers()
