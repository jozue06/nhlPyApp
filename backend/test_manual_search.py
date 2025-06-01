#!/usr/bin/env python3

import requests
import predicates
from queryParser import NHL_TEAMS, create_player_from_api_data, processQueryStringJSON


def manual_goalie_search():
    """Manually implement what processQueryStringJSON should do for goalies"""
    print("Manual goalie search across first 5 teams...")

    # Set up filters like processQueryStringJSON does
    usePositionFilter = True
    positionFilter = ["G"]

    # Other filters (all false for this test)
    useCountryCode = False
    countriesToSearchFor = []
    useExcludeCountryCode = False
    countriesToExclude = []
    useRankFilter = False
    rankFilter = 0
    useNegRankFilter = False
    printOnlyEligable = False
    useHandFilter = False
    handFilter = ""
    useHeightFilter = False
    heightFilter = 0
    useNegHeightFilter = False
    weightFilter = 0
    useNegWeightFilter = False
    useAgeFilter = False
    ageFilter = 0
    useNegAgeFilter = False

    all_filtered_players = []

    # Loop through first 5 teams to get prospects
    for team_abbrev in NHL_TEAMS[:5]:
        print(f"Processing team {team_abbrev}...")
        try:
            response = requests.get(
                f"https://api-web.nhle.com/v1/prospects/{team_abbrev}"
            )
            if response.status_code == 200:
                team_data = response.json()

                # Process all positions to get all prospects
                team_prospects = []
                for position_group in ["forwards", "defensemen", "goalies"]:
                    if position_group in team_data:
                        for player in team_data[position_group]:
                            converted_player = create_player_from_api_data(player)
                            team_prospects.append(converted_player)

                print(f"  Found {len(team_prospects)} total prospects")

                # Filter prospects using the same logic as processQueryStringJSON
                team_filtered = []
                for p in team_prospects:
                    if predicates.all(
                        p,
                        useCountryCode,
                        countriesToSearchFor,
                        useExcludeCountryCode,
                        countriesToExclude,
                        useRankFilter,
                        rankFilter,
                        useNegRankFilter,
                        printOnlyEligable,
                        usePositionFilter,
                        positionFilter,
                        useHandFilter,
                        handFilter,
                        useHeightFilter,
                        heightFilter,
                        useNegHeightFilter,
                        weightFilter,
                        useNegWeightFilter,
                        useAgeFilter,
                        ageFilter,
                        useNegAgeFilter,
                    ):
                        all_filtered_players.append(p)
                        team_filtered.append(p["fullName"])

                print(f"  Filtered to {len(team_filtered)} players: {team_filtered}")
            else:
                print(f"  API call failed: {response.status_code}")
        except Exception as e:
            print(f"  Error: {e}")

    print(f"\nTotal players after filtering: {len(all_filtered_players)}")

    # Display results
    if all_filtered_players:
        print(f"Manual search found {len(all_filtered_players)} goalies:")
        for i, player in enumerate(all_filtered_players):
            print(f"  {i+1}: {player.get('fullName')} - {player.get('primaryPosition', {}).get('abbreviation')}")
    else:
        print("No players found!")

    # Compare with processQueryStringJSON
    print("\nComparing with processQueryStringJSON('-POS G'):")
    try:
        result = processQueryStringJSON("-POS G")
        players = result.get("players", [])
        print(f"processQueryStringJSON found {len(players)} goalies")
        if len(players) > 0:
            print("First 5 from processQueryStringJSON:")
            for i, player in enumerate(players[:5]):
                print(f"  {i+1}: {player.get('fullName')} - {player.get('primaryPosition', {}).get('abbreviation')}")
    except Exception as e:
        print(f"Error with processQueryStringJSON: {e}")


if __name__ == "__main__":
    manual_goalie_search()
