import requests
import re

import predicates
from playerClass import Player
from processPlayers import processPlayersToJSON
from sorting import sort

# NHL team abbreviations for looping through all teams
NHL_TEAMS = [
    "ANA",
    "BOS",
    "BUF",
    "CGY",
    "CAR",
    "CHI",
    "COL",
    "CBJ",
    "DAL",
    "DET",
    "EDM",
    "FLA",
    "LAK",
    "MIN",
    "MTL",
    "NSH",
    "NJD",
    "NYI",
    "NYR",
    "OTT",
    "PHI",
    "PIT",
    "SJS",
    "SEA",
    "STL",
    "TBL",
    "TOR",
    "UTA",
    "VAN",
    "VGK",
    "WSH",
    "WPG",
]


def processQueryString(queryString):
    partsToReturn = []

    parts = queryString.rstrip().split(" ")

    for part in parts:
        if "-" in part:
            partsToReturn.append(part)
        elif "," in part:
            subArr = []
            for sub in part.split(","):
                subArr.append(sub.replace('"', ""))
            partsToReturn.append(subArr)
        else:
            partsToReturn.append([part.replace('"', "")])

    return partsToReturn


def format_height_from_inches(heightInInches):
    """Convert inches to feet'inches" format"""
    if not heightInInches:
        return None
    feet = heightInInches // 12
    inches = heightInInches % 12
    return f"{feet}'{inches}\""


def get_position_info(positionCode):
    """Convert position code to full position info"""
    position_map = {
        "C": {"name": "Center", "abbreviation": "C"},
        "L": {"name": "Left Wing", "abbreviation": "LW"},
        "R": {"name": "Right Wing", "abbreviation": "RW"},
        "D": {"name": "Defenseman", "abbreviation": "D"},
        "G": {"name": "Goalie", "abbreviation": "G"},
    }
    return position_map.get(positionCode, {"name": positionCode, "abbreviation": positionCode})


def create_player_from_api_data(player_data):
    """Create a standardized player object from NHL API data"""
    # Extract name
    firstName = player_data.get('firstName', {}).get('default', '') if player_data.get('firstName') else ''
    lastName = player_data.get('lastName', {}).get('default', '') if player_data.get('lastName') else ''
    fullName = f"{firstName} {lastName}".strip()

    # Get position info
    positionCode = player_data.get("positionCode", "")
    primaryPosition = get_position_info(positionCode)

    # Format height
    height = format_height_from_inches(player_data.get("heightInInches"))

    return {
        "id": player_data.get("id"),
        "fullName": fullName,
        "firstName": firstName,
        "lastName": lastName,
        "birthDate": player_data.get("birthDate", ""),
        "height": height,
        "heightInInches": player_data.get("heightInInches"),
        "weight": player_data.get("weightInPounds"),
        "birthCountry": player_data.get("birthCountry", ""),
        "headshot": player_data.get("headshot", ""),
        "primaryPosition": primaryPosition,
        "positionCode": positionCode,
        "shootsCatches": player_data.get("shootsCatches", ""),
        "draftStatus": "Eligible",  # Default since new API doesn't provide this
        "ranks": {},  # Not provided in new API
    }


def processQueryStringJSON(queryString):
    """Process query string and return JSON results"""
    results = []
    playerList = []
    filter_info = []

    # Initialize all filter variables
    usePositionFilter = False
    useHandFilter = False
    useHeightFilter = False
    useWeightFilter = False
    useAgeFilter = False
    useRankFilter = False
    useCountryCode = False
    useExcludeCountryCode = False
    useIdFilter = False
    useNegHeightFilter = False
    useNegWeightFilter = False
    useNegAgeFilter = False
    useNegRankFilter = False
    printOnlyRanked = False
    printOnlyEligable = False

    positionFilter = []
    handFilter = ""
    heightFilter = 0
    weightFilter = 0
    ageFilter = 0
    rankFilter = 0
    countriesToSearchFor = []
    countriesToExclude = []
    filterNameForSorting = ""

    # Parse the query string if provided
    if queryString and len(queryString.strip()) > 0:
        queryString = processQueryString(queryString.upper())

        # Check for help - match the original logic that checks for -H or -h
        if "-H" in queryString or "-h" in queryString:
            return {
                "isHelp": True,
                "messages": [
                    "-H: Show help",
                    "-CODES <country_codes>: Filter by birth country codes",
                    "-EXCLUDE-CODES <country_codes>: Exclude birth country codes",
                    "-HEIGHT <height>: Filter by height (inches)",
                    "-AGE <age>: Filter by age",
                    "-WEIGHT <weight>: Filter by weight (lbs)",
                    "-POS <positions>: Filter by position (C, LW, RW, D, G)",
                    "-HAND <L/R>: Filter by shooting/catching hand",
                    "-RANKED: Show only ranked players",
                    "-MAX-RANK <rank>: Maximum rank filter",
                    "-MIN-RANK <rank>: Minimum rank filter",
                    "-ELIG: Show only draft eligible players"
                ]
            }

        # Now process filters using the same logic as HTML version
        useIdFilter = "-ID" in queryString
        useCountryCode = "-CODES" in queryString
        countriesToSearchFor = (
            queryString[queryString.index("-CODES") + 1] if useCountryCode else []
        )

        useExcludeCountryCode = "-EXCLUDE-CODES" in queryString
        countriesToExclude = (
            queryString[queryString.index("-EXCLUDE-CODES") + 1]
            if useExcludeCountryCode
            else []
        )

        useNegHeightFilter = "-HEIGHT" in queryString
        usePlusHeightFilter = "+HEIGHT" in queryString
        heightFilter = ""
        if useNegHeightFilter:
            heightFilter = queryString[queryString.index("-HEIGHT") + 1][0]
            filterNameForSorting = "-HEIGHT"
        elif usePlusHeightFilter:
            heightFilter = queryString[queryString.index("+HEIGHT") + 1][0]
            filterNameForSorting = "+HEIGHT"
        useHeightFilter = len(heightFilter) > 0

        useNegAgeFilter = "-AGE" in queryString
        usePlusAgeFilter = "+AGE" in queryString
        ageFilter = ""
        if useNegAgeFilter:
            ageFilter = queryString[queryString.index("-AGE") + 1][0]
            filterNameForSorting = "-AGE"
        elif usePlusAgeFilter:
            ageFilter = queryString[queryString.index("+AGE") + 1][0]
            filterNameForSorting = "+AGE"
        useAgeFilter = len(ageFilter) > 0

        useNegWeightFilter = "-WEIGHT" in queryString
        usePlusWeightFilter = "+WEIGHT" in queryString
        weightFilter = ""
        if useNegWeightFilter:
            weightFilter = queryString[queryString.index("-WEIGHT") + 1][0]
            filterNameForSorting = "-WEIGHT"
        elif usePlusWeightFilter:
            weightFilter = queryString[queryString.index("+WEIGHT") + 1][0]
            filterNameForSorting = "+WEIGHT"
        useWeightFilter = len(weightFilter) > 0

        printOnlyRanked = "-RANKED" in queryString
        if printOnlyRanked:
            filterNameForSorting = "-RANK"

        useNegRankFilter = "-MAX-RANK" in queryString
        usePlusRankFilter = "-MIN-RANK" in queryString
        rankFilter = 0
        if useNegRankFilter:
            rankFilter = queryString[queryString.index("-MAX-RANK") + 1][0]
            filterNameForSorting = "-MAX-RANK"
        elif usePlusRankFilter:
            rankFilter = queryString[queryString.index("-MIN-RANK") + 1][0]
            filterNameForSorting = "-MIN-RANK"

        useRankFilter = int(rankFilter) > 0

        if useRankFilter:
            printOnlyRanked = True
            filterNameForSorting = "-RANK"

        printOnlyEligable = "-ELIG" in queryString

        usePositionFilter = "-POS" in queryString
        positionFilter = (
            queryString[queryString.index("-POS") + 1] if usePositionFilter else []
        )
        if usePositionFilter and positionFilter[0].upper() == "F":
            positionFilter[0] = "RW"
            positionFilter.append("C")
            positionFilter.append("LW")

        useHandFilter = "-HAND" in queryString
        handFilter = queryString[queryString.index("-HAND") + 1][0] if useHandFilter else ""

    # Build filter information to display to user
    if useIdFilter:
        # Handle ID filter
        nhlPlayerId = (
            queryString[queryString.index("-ID") + 1][0] if useIdFilter else ""
        )
        filter_info.append(f"Using Player NHL ID Filter: {nhlPlayerId}")
    elif (useCountryCode or useExcludeCountryCode or useNegHeightFilter or usePlusHeightFilter or
          useNegAgeFilter or usePlusAgeFilter or useNegWeightFilter or usePlusWeightFilter or
          printOnlyRanked or useNegRankFilter or usePlusRankFilter or useRankFilter or
          printOnlyEligable or usePositionFilter or useHandFilter):
        # Display active filters
        if len(countriesToSearchFor) > 0:
            filter_info.append(f"Searching Birth Country Codes: {countriesToSearchFor}")

        if len(countriesToExclude) > 0:
            filter_info.append(f"Excluding Birth Country Codes: {countriesToExclude}")

        filter_info.append(f"Print Only Ranked Players: {printOnlyRanked}")
        filter_info.append(f"Print Only Draft Eligable Players: {printOnlyEligable}")

        if usePositionFilter:
            filter_info.append(f"Using Position Filter: {positionFilter}")

        if useHandFilter:
            filter_info.append(f"Using Hand / Side Filter: {handFilter}")

        if useWeightFilter:
            weightFilterEquality = "<=" if useNegWeightFilter else ">="
            filter_info.append(f"Using Weight Filter: {weightFilterEquality} {weightFilter}")

        if useHeightFilter:
            heightFilterEquality = "<=" if useNegHeightFilter else ">="
            filter_info.append(f"Using Height Filter: {heightFilterEquality} {heightFilter}")

        if useAgeFilter:
            ageFilterEquality = "<=" if useNegAgeFilter else ">="
            filter_info.append(f"Using Age Filter: {ageFilterEquality} {ageFilter}")

        if useRankFilter:
            rankFilterEquality = "<=" if useNegRankFilter else ">="
            filter_info.append(f"Using Rank Filter: {rankFilterEquality} {rankFilter}")
    else:
        filter_info.append("Showing all prospects (no filters applied)")

    # Get real data from NHL API
    all_prospects = []
    playerList = []

    if useIdFilter:
        # Handle single player lookup by ID
        nhlPlayerId = (
            queryString[queryString.index("-ID") + 1][0] if useIdFilter else ""
        )

        found_player = None
        for team_abbrev in NHL_TEAMS:
            try:
                response = requests.get(
                    f"https://api-web.nhle.com/v1/prospects/{team_abbrev}"
                )
                if response.status_code == 200:
                    team_data = response.json()

                    # Search in all position arrays
                    for position_group in ["forwards", "defensemen", "goalies"]:
                        if position_group in team_data:
                            for player in team_data[position_group]:
                                if str(player.get("id")) == str(nhlPlayerId):
                                    found_player = create_player_from_api_data(player)
                                    break
                    if found_player:
                        break
            except Exception as e:
                print(f"Error searching for player in team {team_abbrev}: {e}")

        if found_player:
            newPlayer = Player(found_player)
            playerList.append(newPlayer)
        else:
            return {
                "players": [],
                "filterInfo": filter_info,
                "error": f"Player not found with ID: {nhlPlayerId}"
            }
    elif (useCountryCode or useExcludeCountryCode or useNegHeightFilter or usePlusHeightFilter or
          useNegAgeFilter or usePlusAgeFilter or useNegWeightFilter or usePlusWeightFilter or
          printOnlyRanked or useNegRankFilter or usePlusRankFilter or useRankFilter or
          printOnlyEligable or usePositionFilter or useHandFilter) and not useIdFilter:
        # Get all prospects for filtering
        for team_abbrev in NHL_TEAMS:
            try:
                response = requests.get(
                    f"https://api-web.nhle.com/v1/prospects/{team_abbrev}"
                )
                if response.status_code == 200:
                    team_data = response.json()

                    # Process forwards
                    if "forwards" in team_data:
                        for player in team_data["forwards"]:
                            player_obj = create_player_from_api_data(player)
                            all_prospects.append(player_obj)

                    # Process defensemen
                    if "defensemen" in team_data:
                        for player in team_data["defensemen"]:
                            player_obj = create_player_from_api_data(player)
                            all_prospects.append(player_obj)

                    # Process goalies
                    if "goalies" in team_data:
                        for player in team_data["goalies"]:
                            player_obj = create_player_from_api_data(player)
                            all_prospects.append(player_obj)
                else:
                    print(f"Warning: Failed to get prospects for team {team_abbrev}")
            except Exception as e:
                print(f"Error getting prospects for team {team_abbrev}: {e}")

        # Filter prospects using existing predicates logic
        for p in all_prospects:
            if predicates.all(
                p,
                useCountryCode, countriesToSearchFor,
                useExcludeCountryCode, countriesToExclude,
                useRankFilter, rankFilter, useNegRankFilter,
                printOnlyEligable,
                usePositionFilter, positionFilter,
                useHandFilter, handFilter,
                useHeightFilter, heightFilter, useNegHeightFilter,
                useWeightFilter, weightFilter, useNegWeightFilter,
                useAgeFilter, ageFilter, useNegAgeFilter,
            ):
                newPlayer = Player(p)
                playerList.append(newPlayer)
    else:
        # No specific filters applied - show all prospects
        for team_abbrev in NHL_TEAMS:
            try:
                response = requests.get(
                    f"https://api-web.nhle.com/v1/prospects/{team_abbrev}"
                )
                if response.status_code == 200:
                    team_data = response.json()

                    # Process forwards
                    if "forwards" in team_data:
                        for player in team_data["forwards"]:
                            player_obj = create_player_from_api_data(player)
                            all_prospects.append(player_obj)

                    # Process defensemen
                    if "defensemen" in team_data:
                        for player in team_data["defensemen"]:
                            player_obj = create_player_from_api_data(player)
                            all_prospects.append(player_obj)

                    # Process goalies
                    if "goalies" in team_data:
                        for player in team_data["goalies"]:
                            player_obj = create_player_from_api_data(player)
                            all_prospects.append(player_obj)
                else:
                    print(f"Warning: Failed to get prospects for team {team_abbrev}")
            except Exception as e:
                print(f"Error getting prospects for team {team_abbrev}: {e}")

        # Add all prospects without filtering
        for p in all_prospects:
            newPlayer = Player(p)
            playerList.append(newPlayer)

    # Return JSON with both player data and filter information
    return {
        "players": processPlayersToJSON(sort(playerList, filterName=filterNameForSorting)),
        "filterInfo": filter_info
    }
