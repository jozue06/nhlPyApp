#!/usr/bin/env python3

import requests
from queryParser import convert_api_response_to_old_format
import predicates

def debug_predicates():
    """Debug each predicate function individually"""
    print("Debugging predicate functions...")
    
    # Get one goalie to test
    response = requests.get("https://api-web.nhle.com/v1/prospects/TOR")
    if response.status_code == 200:
        data = response.json()
        if 'goalies' in data and data['goalies']:
            goalie_raw = data['goalies'][0]
            goalie = convert_api_response_to_old_format(goalie_raw)
            
            print(f"Testing with goalie: {goalie['fullName']}")
            print(f"Position: {goalie['primaryPosition']}")
            print(f"Raw goalie data keys: {list(goalie.keys())}")
            print(f"Sample values:")
            for key, value in goalie.items():
                print(f"  {key}: {repr(value)}")
            
            # Test each filter function individually
            print("\nTesting individual filter functions:")
            
            # Set up the same parameters as the failing test
            useCountryCode = False
            countriesToSearchFor = []
            useRankFilter = False
            rankFilter = 0
            useNegRankFilter = False
            printOnlyEligable = False
            usePositionFilter = True
            positionFilter = ['G']
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
            
            # Test each filter
            print(f"1. filterOne (country): {predicates.filterOne(useCountryCode, goalie, countriesToSearchFor)}")
            print(f"2. filterTwo (rank): {predicates.filterTwo(useRankFilter, goalie, rankFilter, useNegRankFilter)}")
            print(f"3. filterThree (eligibility): {predicates.filterThree(printOnlyEligable, goalie)}")
            print(f"4. filterFour (position): {predicates.filterFour(usePositionFilter, positionFilter, goalie)}")
            print(f"5. filterFive (hand): {predicates.filterFive(useHandFilter, goalie, handFilter)}")
            print(f"6. filterSix (height): {predicates.filterSix(useHeightFilter, goalie, heightFilter, useNegHeightFilter)}")
            print(f"7. filterSeven (weight): {predicates.filterSeven(useNegWeightFilter, goalie, weightFilter, useNegWeightFilter)}")
            print(f"8. filterEight (age): {predicates.filterEight(useAgeFilter, goalie, ageFilter, useNegAgeFilter)}")
            print(f"9. filterNine (league): {predicates.filterNine(useLeagueFilter, goalie, leaguesFilter)}")
            print(f"10. filterTen (team): {predicates.filterTen(useTeamFilter, goalie, teamsFilter)}")
            
            # Test the combined function
            all_result = predicates.all(
                goalie,  
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
                teamsFilter
            )
            
            print(f"\nCombined result: {all_result}")

if __name__ == "__main__":
    debug_predicates() 