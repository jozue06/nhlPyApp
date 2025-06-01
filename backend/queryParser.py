import requests
import re

import predicates
from playerClass import Player
from processPlayers import processPlayers
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


def convert_api_response_to_old_format(player_data):
    """Convert new API response format to match the old format expected by the rest of the code"""
    converted = {
        "id": player_data.get("id"),
        "fullName": f"{player_data.get('firstName', {}).get('default', '')} {player_data.get('lastName', {}).get('default', '')}".strip(),
        "birthDate": player_data.get("birthDate", ""),
        "height": (
            f"{player_data.get('heightInInches', 0) // 12}'{player_data.get('heightInInches', 0) % 12}\""
            if player_data.get("heightInInches")
            else None
        ),
        "weight": player_data.get("weightInPounds"),
        "birthCountry": player_data.get("birthCountry", ""),
        "headshot": player_data.get("headshot", ""),  # Add headshot URL
        "primaryPosition": {
            "name": {
                "C": "Center",
                "L": "Left Wing",
                "R": "Right Wing",
                "D": "Defenseman",
                "G": "Goalie",
            }.get(
                player_data.get("positionCode", ""), player_data.get("positionCode", "")
            ),
            "abbreviation": player_data.get("positionCode", ""),
        },
        "shootsCatches": player_data.get("shootsCatches", ""),
        "draftStatus": "Eligible",  # Default since new API doesn't provide this
        "ranks": {},  # Not provided in new API
    }
    return converted


def processIntoHtml(queryString):
    results = []
    filterNameForSorting = "-NAME"

    queryString = processQueryString(queryString.upper())

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

    playerList = []
    if "-H" in queryString or "-h" in queryString:
        results.append("\n")
        results.append(
            "****************************THE HELP MENU****************************"
        )
        results.append("\n")
        results.append("To Show Ranked Players Only add -RANKED")
        results.append("To Show Draft Eligable Players Only add -ELIG")
        results.append("\n")
        results.append(
            'To Use the Country Code Filter add -CODES followed directly by "codeOne,codeTwo"'
        )
        results.append(
            'To Exclude Country Codes add -EXCLUDE-CODES followed directly by "codeOne,codeTwo"'
        )
        results.append(
            'To Use the Position Filter add -POS followed directly by "c" or "g" (c for center, g for goalie etc.)'
        )
        results.append(
            'To Use the Hand Filter add -HAND followed directly by "l" or "r"'
        )
        results.append("\n")
        results.append(
            'To Use the Less Than Or Equal to Age Filter add -AGE followed directly by "the maximum age"'
        )
        results.append(
            'To Use the Greater Than Or Equal to Age Filter add +AGE followed directly by "the minimum age"'
        )
        results.append("\n")
        results.append(
            'To Use the Less Than Or Equal to Height Filter add -HEIGHT followed directly by "the maximum height"'
        )
        results.append(
            'To Use the Greater Than Or Equal to Height Filter add +HEIGHT followed directly by "the minimum height"'
        )
        results.append("\n")
        results.append(
            'To Use the Less Than Or Equal to Weight Filter add -WEIGHT followed directly by "the maximum weight"'
        )
        results.append(
            'To Use the Greater Than Or Equal to Weight Filter add +WEIGHT followed directly by "the minimum weight"'
        )
        results.append("\n")
        results.append(
            'To Use the Less Than Or Equal to Rank Filter add -MAX-RANK followed directly by "the maximum rank"'
        )
        results.append(
            'To Use the Greater Than Or Equal to Rank Filter add -MIN-RANK followed directly by "the minimum rank"'
        )
        results.append("\n")
        results.append(
            'To Show A Single Player Info By NHL Player ID add -ID followed directly by "the players nhl id"'
        )
        results.append("\n")
        results.append(
            "*********************************************************************"
        )
        results.append("\n")
    elif (
        useCountryCode
        or useExcludeCountryCode
        or useNegHeightFilter
        or usePlusHeightFilter
        or useNegAgeFilter
        or usePlusAgeFilter
        or useNegWeightFilter
        or usePlusWeightFilter
        or printOnlyRanked
        or useNegRankFilter
        or usePlusRankFilter
        or useRankFilter
        or printOnlyEligable
        or usePositionFilter
        or useHandFilter
    ) and not useIdFilter:
        results.append("\n")

        if len(countriesToSearchFor) > 0:
            results.append(
                "Searching Birth Country Codes: " + str(countriesToSearchFor)
            )

        if len(countriesToExclude) > 0:
            results.append("Excluding Birth Country Codes: " + str(countriesToExclude))

        results.append("Print Only Ranked Players: " + str(printOnlyRanked))
        results.append("Print Only Draft Eligable Players: " + str(printOnlyEligable))

        if usePositionFilter:
            results.append("Using Position Filter: " + str(positionFilter))

        if useHandFilter:
            results.append("Using Hand / Side Filter: " + str(handFilter))

        weightFilterEquality = "<=" if useNegWeightFilter else ">="

        if useWeightFilter:
            results.append(
                "Using Weight Filter: " + weightFilterEquality + " " + str(weightFilter)
            )

        heightFilterEquality = "<=" if useNegHeightFilter else ">="

        if useHeightFilter:
            results.append(
                "Using Height Filter: " + heightFilterEquality + " " + str(heightFilter)
            )

        ageFilterEquality = "<=" if useNegAgeFilter else ">="

        if useAgeFilter:
            results.append(
                "Using Age Filter: " + ageFilterEquality + " " + str(ageFilter)
            )

        rankFilterEquality = "<=" if useNegRankFilter else ">="

        if useRankFilter:
            results.append(
                "Using Rank Filter: " + rankFilterEquality + " " + str(rankFilter)
            )

        # Loop through all NHL teams to get prospects
        all_prospects = []
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
                            converted_player = convert_api_response_to_old_format(
                                player
                            )
                            all_prospects.append(converted_player)

                    # Process defensemen
                    if "defensemen" in team_data:
                        for player in team_data["defensemen"]:
                            converted_player = convert_api_response_to_old_format(
                                player
                            )
                            all_prospects.append(converted_player)

                    # Process goalies
                    if "goalies" in team_data:
                        for player in team_data["goalies"]:
                            converted_player = convert_api_response_to_old_format(
                                player
                            )
                            all_prospects.append(converted_player)
                else:
                    print(f"Warning: Failed to get prospects for team {team_abbrev}")
            except Exception as e:
                print(f"Error getting prospects for team {team_abbrev}: {e}")

        # Filter prospects using existing logic
        for p in all_prospects:
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
                useWeightFilter,
                weightFilter,
                useNegWeightFilter,
                useAgeFilter,
                ageFilter,
                useNegAgeFilter,
            ):
                newPlayer = Player(p=p)
                playerList.append(newPlayer)
        processPlayers(sort(playerList, filterName=filterNameForSorting), results)
    elif useIdFilter:
        nhlPlayerId = (
            queryString[queryString.index("-ID") + 1][0] if useIdFilter else ""
        )

        results.append("\n")
        results.append("Using Player NHL ID Filter: " + nhlPlayerId)

        # For individual player lookup, we need to search through all teams
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
                                    found_player = convert_api_response_to_old_format(
                                        player
                                    )
                                    break
                    if found_player:
                        break
            except Exception as e:
                print(f"Error searching for player in team {team_abbrev}: {e}")

        if found_player:
            newPlayer = Player(p=found_player)
            playerList.append(newPlayer)
            processPlayers(playerList, results)
        else:
            results.append("Player not found with ID: " + nhlPlayerId)
    else:
        # No specific filters applied - show all prospects
        results.append("\n")
        results.append("Showing all prospects (no filters applied)")

        # Loop through all NHL teams to get prospects
        all_prospects = []
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
                            converted_player = convert_api_response_to_old_format(
                                player
                            )
                            all_prospects.append(converted_player)

                    # Process defensemen
                    if "defensemen" in team_data:
                        for player in team_data["defensemen"]:
                            converted_player = convert_api_response_to_old_format(
                                player
                            )
                            all_prospects.append(converted_player)

                    # Process goalies
                    if "goalies" in team_data:
                        for player in team_data["goalies"]:
                            converted_player = convert_api_response_to_old_format(
                                player
                            )
                            all_prospects.append(converted_player)
                else:
                    print(f"Warning: Failed to get prospects for team {team_abbrev}")
            except Exception as e:
                print(f"Error getting prospects for team {team_abbrev}: {e}")

        # Add all prospects without filtering
        for p in all_prospects:
            newPlayer = Player(p=p)
            playerList.append(newPlayer)

        processPlayers(sort(playerList, filterName=filterNameForSorting), results)

    return results


def processQueryStringJSON(queryString):
    """Process query string and return JSON results instead of HTML strings"""
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
        queryString = queryString.split()

        # Check for help - match the original logic that checks for -H or -h
        if "-H" in [item.upper() for item in queryString] or any(item.upper() == "-H" for item in queryString):
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

        # Process filters
        for i, item in enumerate(queryString):
            if item.upper() == "-POS":
                usePositionFilter = True
                if i + 1 < len(queryString):
                    positionFilter = queryString[i + 1].split(",")
            elif item.upper() == "-HAND":
                useHandFilter = True
                if i + 1 < len(queryString):
                    handFilter = queryString[i + 1]
            elif item.upper() == "-HEIGHT":
                useHeightFilter = True
                if i + 1 < len(queryString):
                    try:
                        heightFilter = int(queryString[i + 1])
                        if queryString[i + 1].startswith("-"):
                            useNegHeightFilter = True
                            heightFilter = abs(heightFilter)
                    except ValueError:
                        pass
            elif item.upper() == "-WEIGHT":
                useWeightFilter = True
                if i + 1 < len(queryString):
                    try:
                        weightFilter = int(queryString[i + 1])
                        if queryString[i + 1].startswith("-"):
                            useNegWeightFilter = True
                            weightFilter = abs(weightFilter)
                    except ValueError:
                        pass
            elif item.upper() == "-AGE":
                useAgeFilter = True
                if i + 1 < len(queryString):
                    try:
                        ageFilter = int(queryString[i + 1])
                        if queryString[i + 1].startswith("-"):
                            useNegAgeFilter = True
                            ageFilter = abs(ageFilter)
                    except ValueError:
                        pass
            elif item.upper() in ["-RANK", "-MAX-RANK"]:
                useRankFilter = True
                if i + 1 < len(queryString):
                    try:
                        rankFilter = int(queryString[i + 1])
                        if queryString[i + 1].startswith("-"):
                            useNegRankFilter = True
                            rankFilter = abs(rankFilter)
                    except ValueError:
                        pass
            elif item.upper() == "-MIN-RANK":
                useRankFilter = True
                useNegRankFilter = True
                if i + 1 < len(queryString):
                    try:
                        rankFilter = int(queryString[i + 1])
                    except ValueError:
                        pass
            elif item.upper() == "-CODES":
                useCountryCode = True
                if i + 1 < len(queryString):
                    countriesToSearchFor = queryString[i + 1].split(",")
            elif item.upper() == "-EXCLUDE-CODES":
                useExcludeCountryCode = True
                if i + 1 < len(queryString):
                    countriesToExclude = queryString[i + 1].split(",")
            elif item.upper() == "-ID":
                useIdFilter = True
            elif item.upper() == "-RANKED":
                printOnlyRanked = True
            elif item.upper() == "-ELIG":
                printOnlyEligable = True

    # Build filter information to display to user
    if useIdFilter:
        # Handle ID filter
        nhlPlayerId = ""
        for i, item in enumerate(queryString):
            if item.upper() == "-ID" and i + 1 < len(queryString):
                nhlPlayerId = queryString[i + 1]
                break
        filter_info.append(f"Using Player NHL ID Filter: {nhlPlayerId}")
    elif (useCountryCode or useExcludeCountryCode or useHeightFilter or useWeightFilter or
          useAgeFilter or useRankFilter or printOnlyRanked or printOnlyEligable or
          usePositionFilter or useHandFilter):
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

    # Get real data from NHL API (always, regardless of filters)
    NHL_TEAMS = [
        "ANA", "BOS", "BUF", "CGY", "CAR", "CHI", "COL", "CBJ",
        "DAL", "DET", "EDM", "FLA", "LAK", "MIN", "MTL", "NSH",
        "NJD", "NYI", "NYR", "OTT", "PHI", "PIT", "SJS", "SEA",
        "STL", "TBL", "TOR", "UTA", "VAN", "VGK", "WSH", "WPG",
    ]

    all_prospects = []

    if useIdFilter:
        # Handle single player lookup by ID
        nhlPlayerId = ""
        for i, item in enumerate(queryString):
            if item.upper() == "-ID" and i + 1 < len(queryString):
                nhlPlayerId = queryString[i + 1]
                break

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
                                    found_player = convert_api_response_to_old_format(
                                        player
                                    )
                                    break
                    if found_player:
                        break
            except Exception as e:
                print(f"Error searching for player in team {team_abbrev}: {e}")

        if found_player:
            newPlayer = Player(p=found_player)
            playerList.append(newPlayer)
        else:
            return {
                "players": [],
                "filterInfo": filter_info,
                "error": f"Player not found with ID: {nhlPlayerId}"
            }
    else:
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
                            converted_player = convert_api_response_to_old_format(
                                player
                            )
                            all_prospects.append(converted_player)

                    # Process defensemen
                    if "defensemen" in team_data:
                        for player in team_data["defensemen"]:
                            converted_player = convert_api_response_to_old_format(
                                player
                            )
                            all_prospects.append(converted_player)

                    # Process goalies
                    if "goalies" in team_data:
                        for player in team_data["goalies"]:
                            converted_player = convert_api_response_to_old_format(
                                player
                            )
                            all_prospects.append(converted_player)
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
                newPlayer = Player(p=p)
                playerList.append(newPlayer)

    # Return JSON with both player data and filter information
    return {
        "players": processPlayersToJSON(sort(playerList, filterName=filterNameForSorting)),
        "filterInfo": filter_info
    }
