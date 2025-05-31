#!/usr/bin/env python3

import requests
from queryParser import convert_api_response_to_old_format, NHL_TEAMS
from playerClass import Player
from processPlayers import processPlayers
from sorting import sort
import predicates

def manual_goalie_search():
    """Manually implement what processIntoHtml should do for goalies"""
    print("Manual goalie search across first 5 teams...")
    
    # Set up filters like processIntoHtml does
    usePositionFilter = True
    positionFilter = ['G']
    
    # Other filters (all false for this test)
    useCountryCode = False
    countriesToSearchFor = []
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
    useLeagueFilter = False
    leaguesFilter = []
    useTeamFilter = False
    teamsFilter = []
    
    playerList = []
    
    # Loop through first 5 teams to get prospects
    for team_abbrev in NHL_TEAMS[:5]:
        print(f"Processing team {team_abbrev}...")
        try:
            response = requests.get(f"https://api-web.nhle.com/v1/prospects/{team_abbrev}")
            if response.status_code == 200:
                team_data = response.json()
                
                # Process all positions to get all prospects
                team_prospects = []
                for position_group in ['forwards', 'defensemen', 'goalies']:
                    if position_group in team_data:
                        for player in team_data[position_group]:
                            converted_player = convert_api_response_to_old_format(player)
                            team_prospects.append(converted_player)
                
                print(f"  Found {len(team_prospects)} total prospects")
                
                # Filter prospects using the same logic as processIntoHtml
                team_filtered = []
                for p in team_prospects:
                    if predicates.all(
                        p,  
                        useCountryCode, 
                        countriesToSearchFor,
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
                        useLeagueFilter,
                        leaguesFilter,
                        useTeamFilter, 
                        teamsFilter):
                            newPlayer = Player(p=p)
                            playerList.append(newPlayer)
                            team_filtered.append(p['fullName'])
                
                print(f"  Filtered to {len(team_filtered)} players: {team_filtered}")
            else:
                print(f"  API call failed: {response.status_code}")
        except Exception as e:
            print(f"  Error: {e}")
    
    print(f"\nTotal players after filtering: {len(playerList)}")
    
    # Process results
    if playerList:
        results = []
        sorted_players = sort(playerList, filterName="-NAME")
        processPlayers(sorted_players, results)
        
        print(f"Final results: {len(results)} lines")
        for i, line in enumerate(results[:20]):
            print(f"  {i+1}: {line}")
    else:
        print("No players found!")

if __name__ == "__main__":
    manual_goalie_search() 