import requests
from sorting import sort
import predicates
from  processPlayers import processPlayers 
from playerClass import Player


def processQueryString(queryString):
	partsToReturn = []

	parts = queryString.rstrip().split(" ")

	for part in parts:
		if "-" in part:
			partsToReturn.append(part)
		elif "," in part:
			subArr = []
			for sub in part.split(","):
				subArr.append(sub.replace("\"",""))
			partsToReturn.append(subArr)
		else:
			partsToReturn.append([part.replace("\"","")])

	return partsToReturn


def processIntoHtml(queryString):
	results = []
	filterNameForSorting = "-NAME"

	queryString = processQueryString(queryString.upper())

	useIdFilter = '-ID' in queryString
	useCountryCode = '-CODES' in queryString
	countriesToSearchFor = queryString[queryString.index('-CODES')+1] if useCountryCode else []

	useNegHeightFilter = '-HEIGHT' in queryString
	usePlusHeightFilter = '+HEIGHT' in queryString
	heightFilter = 0
	if useNegHeightFilter:
		heightFilter = queryString[queryString.index('-HEIGHT')+1][0]
		filterNameForSorting = "-HEIGHT"
	elif usePlusHeightFilter:
		heightFilter = queryString[queryString.index('+HEIGHT')+1][0]
		filterNameForSorting = "+HEIGHT"
	useHeightFilter = int(heightFilter) > 0

	useNegAgeFilter = '-AGE' in queryString
	usePlusAgeFilter = '+AGE' in queryString
	ageFilter = 0
	if useNegAgeFilter:
		ageFilter = queryString[queryString.index('-AGE')+1][0]
		filterNameForSorting = "-AGE"
	elif usePlusAgeFilter:
		ageFilter = queryString[queryString.index('+AGE')+1][0]
		filterNameForSorting = "+AGE"
	useAgeFilter = int(ageFilter) > 0

	useNegWeightFilter = '-WEIGHT' in queryString
	usePlusWeightFilter = '+WEIGHT' in queryString
	weightFilter = 0
	if useNegWeightFilter:
		weightFilter = queryString[queryString.index('-WEIGHT')+1][0]
		filterNameForSorting = "-WEIGHT"
	elif usePlusWeightFilter:
		weightFilter = queryString[queryString.index('+WEIGHT')+1][0]
		filterNameForSorting = "+WEIGHT"

	useWeightFilter = int(weightFilter) > 0

	printOnlyRanked = '-RANKED' in queryString
	if printOnlyRanked:
		filterNameForSorting = "-RANK"

	useNegRankFilter = '-MAX-RANK' in queryString
	usePlusRankFilter = '-MIN-RANK' in queryString
	rankFilter = 0
	if useNegRankFilter:
		rankFilter = queryString[queryString.index('-MAX-RANK')+1][0]
		filterNameForSorting = "-MAX-RANK"
	elif usePlusRankFilter:
		rankFilter = queryString[queryString.index('-MIN-RANK')+1][0]
		filterNameForSorting = "-MIN-RANK"

	useRankFilter = int(rankFilter) > 0

	if useRankFilter:
		printOnlyRanked = True
		filterNameForSorting = "-RANK"

	printOnlyEligable = '-ELIG' in queryString

	usePositionFilter = '-POS' in queryString
	positionFilter = queryString[queryString.index('-POS')+1] if usePositionFilter else [];
	if (positionFilter[0].upper() == "F"):
		positionFilter[0] = "RW"
		positionFilter.append("C")
		positionFilter.append("LW")

	useHandFilter = '-HAND' in queryString
	handFilter = queryString[queryString.index('-HAND')+1][0] if useHandFilter else "";

	useLeagueFilter = '-LEAGUES' in queryString
	leaguesFilter = queryString[queryString.index('-LEAGUES')+1] if useLeagueFilter else [];

	if useLeagueFilter:
		filterNameForSorting = "-LEAGUES"

	useTeamFilter = '-TEAMS' in queryString
	teamsFilter = queryString[queryString.index('-TEAMS')+1] if useTeamFilter else [];
	if useTeamFilter:
		filterNameForSorting = "-TEAMS"
	playerList = []
	if "-H" in queryString or "-h" in queryString:
		results.append("\n")
		results.append("****************************THE HELP MENU****************************")
		results.append("\n")
		results.append("To Show Ranked Players Only add -RANKED")
		results.append("To Show Draft Eligable Players Only add -ELIG")
		results.append("\n")
		results.append("To Use the Country Code Filter add -CODES followed directly by \"codeOne,codeTwo\"")
		results.append("To Use the League Filter add -LEAGUES followed directly by \"league one name,league two name\"")
		results.append("To Use the Team Filter add -TEAMS followed directly by \"team one name,team two name\"")
		results.append("To Use the Position Filter add -POS followed directly by \"c\" or \"g\" (c for center, g for goalie etc.)")
		results.append("To Use the Hand Filter add -HAND followed directly by \"l\" or \"r\"")
		results.append("\n")
		results.append("To Use the Less Than Or Equal to Age Filter add -AGE followed directly by \"the maximum age\"")
		results.append("To Use the Greater Than Or Equal to Age Filter add +AGE followed directly by \"the minimum age\"")
		results.append("\n")
		results.append("To Use the Less Than Or Equal to Height Filter add -HEIGHT followed directly by \"the maximum height\"")
		results.append("To Use the Greater Than Or Equal to Height Filter add +HEIGHT followed directly by \"the minimum height\"")
		results.append("\n")
		results.append("To Use the Less Than Or Equal to Weight Filter add -WEIGHT followed directly by \"the maximum weight\"")
		results.append("To Use the Greater Than Or Equal to Weight Filter add +WEIGHT followed directly by \"the minimum weight\"")
		results.append("\n")
		results.append("To Use the Less Than Or Equal to Rank Filter add -MAX-RANK followed directly by \"the maximum rank\"")
		results.append("To Use the Greater Than Or Equal to Rank Filter add -MIN-RANK followed directly by \"the minimum rank\"")
		results.append("\n")
		results.append("To Show A Single Player Info By NHL Player ID add -ID followed directly by \"the players nhl id\"")
		results.append("\n")
		results.append("*********************************************************************")
		results.append("\n")
	elif (useCountryCode or \
		useNegHeightFilter or \
		usePlusHeightFilter or \
		useNegAgeFilter or \
		usePlusAgeFilter or \
		useNegWeightFilter or \
		usePlusWeightFilter or \
		printOnlyRanked or \
		useNegRankFilter or \
		usePlusRankFilter or \
		useRankFilter or \
		printOnlyEligable or \
		usePositionFilter or \
		useHandFilter or \
		useLeagueFilter or \
		useTeamFilter) and not useIdFilter:
		results.append("\n")

		if len(countriesToSearchFor) > 0:
			results.append("Searching Birth Country Codes: " + str(countriesToSearchFor))

		results.append("Print Only Ranked Players: " + str(printOnlyRanked))
		results.append("Print Only Draft Eligable Players: " + str(printOnlyEligable))

		if usePositionFilter:
			results.append("Using Position Filter: " + str(positionFilter))

		if useHandFilter:
			results.append("Using Hand / Side Filter: " + str(handFilter))

		weightFilterEquality = "<=" if useNegWeightFilter else ">="

		if useWeightFilter:
			results.append("Using Weight Filter: " + weightFilterEquality + " " + str(weightFilter))

		heightFilterEquality = "<=" if useNegHeightFilter else ">="

		if useHeightFilter:
			results.append("Using Height Filter: " + heightFilterEquality + " " + str(heightFilter))

		ageFilterEquality = "<=" if useNegAgeFilter else ">="

		if useAgeFilter:
			results.append("Using Age Filter: " + ageFilterEquality + " " + str(ageFilter))

		rankFilterEquality = "<=" if useNegRankFilter else ">="

		if useRankFilter:
			results.append("Using Rank Filter: " + rankFilterEquality + " " + str(rankFilter))

		if len(leaguesFilter) > 0:
			results.append("Using Leagues Filter: " + str(leaguesFilter))

		if len(teamsFilter) > 0:
			results.append("Using Leagues Filter: " + str(teamsFilter))

		response = requests.get("https://statsapi.web.nhl.com/api/v1/draft/prospects")
		
		
		for p in response.json()['prospects']:
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
		processPlayers(sort(playerList, filterName=filterNameForSorting), results)		
	elif useIdFilter:
		nhlPlayerId = queryString[queryString.index('-ID')+1][0] if useIdFilter else ""

		results.append("\n")
		results.append("Using Player NHL ID Filter: " + nhlPlayerId)

		response = requests.get("https://statsapi.web.nhl.com/api/v1/draft/prospects/" + nhlPlayerId)

		json = response.json()['prospects']
		for p in json:
			newPlayer = Player(p=p)
			playerList.append(newPlayer)

		processPlayers(playerList, results)

	return results



def processIntoJSON(queryString):
	results = []
	filterNameForSorting = "-NAME"

	queryString = processQueryString(queryString.upper())

	useIdFilter = '-ID' in queryString
	useCountryCode = '-CODES' in queryString
	countriesToSearchFor = queryString[queryString.index('-CODES')+1] if useCountryCode else []

	useNegHeightFilter = '-HEIGHT' in queryString
	usePlusHeightFilter = '+HEIGHT' in queryString
	heightFilter = 0
	if useNegHeightFilter:
		heightFilter = queryString[queryString.index('-HEIGHT')+1][0]
		filterNameForSorting = "-HEIGHT"
	elif usePlusHeightFilter:
		heightFilter = queryString[queryString.index('+HEIGHT')+1][0]
		filterNameForSorting = "+HEIGHT"
	useHeightFilter = int(heightFilter) > 0

	useNegAgeFilter = '-AGE' in queryString
	usePlusAgeFilter = '+AGE' in queryString
	ageFilter = 0
	if useNegAgeFilter:
		ageFilter = queryString[queryString.index('-AGE')+1][0]
		filterNameForSorting = "-AGE"
	elif usePlusAgeFilter:
		ageFilter = queryString[queryString.index('+AGE')+1][0]
		filterNameForSorting = "+AGE"
	useAgeFilter = int(ageFilter) > 0

	useNegWeightFilter = '-WEIGHT' in queryString
	usePlusWeightFilter = '+WEIGHT' in queryString
	weightFilter = 0
	if useNegWeightFilter:
		weightFilter = queryString[queryString.index('-WEIGHT')+1][0]
		filterNameForSorting = "-WEIGHT"
	elif usePlusWeightFilter:
		weightFilter = queryString[queryString.index('+WEIGHT')+1][0]
		filterNameForSorting = "+WEIGHT"

	useWeightFilter = int(weightFilter) > 0

	printOnlyRanked = '-RANKED' in queryString

	useNegRankFilter = '-MAX-RANK' in queryString
	usePlusRankFilter = '-MIN-RANK' in queryString
	rankFilter = 0
	if useNegRankFilter:
		rankFilter = queryString[queryString.index('-MAX-RANK')+1][0]
		filterNameForSorting = "-MAX-RANK"
	elif usePlusRankFilter:
		rankFilter = queryString[queryString.index('-MIN-RANK')+1][0]
		filterNameForSorting = "-MIN-RANK"

	useRankFilter = int(rankFilter) > 0

	if useRankFilter:
		printOnlyRanked = True
		filterNameForSorting = "-RANK"
	if printOnlyRanked:
		filterNameForSorting = "-RANK"
	printOnlyEligable = '-ELIG' in queryString

	usePositionFilter = '-POS' in queryString
	positionFilter = queryString[queryString.index('-POS')+1][0] if usePositionFilter else "";

	useHandFilter = '-HAND' in queryString
	handFilter = queryString[queryString.index('-HAND')+1][0] if useHandFilter else "";

	useLeagueFilter = '-LEAGUES' in queryString
	leaguesFilter = queryString[queryString.index('-LEAGUES')+1] if useLeagueFilter else [];

	if useLeagueFilter:
		filterNameForSorting = "-LEAGUES"

	useTeamFilter = '-TEAMS' in queryString
	teamsFilter = queryString[queryString.index('-TEAMS')+1] if useTeamFilter else [];
	if useTeamFilter:
		filterNameForSorting = "-TEAMS"
	playerList = []
	if "-H" in queryString or "-h" in queryString:
		results.append("\n")
		results.append("****************************THE HELP MENU****************************")
		results.append("\n")
		results.append("To Show Ranked Players Only add -RANKED")
		results.append("To Show Draft Eligable Players Only add -ELIG")
		results.append("\n")
		results.append("To Use the Country Code Filter add -CODES followed directly by \"codeOne,codeTwo\"")
		results.append("To Use the League Filter add -LEAGUES followed directly by \"league one name,league two name\"")
		results.append("To Use the Team Filter add -TEAMS followed directly by \"team one name,team two name\"")
		results.append("To Use the Position Filter add -POS followed directly by \"c\" or \"g\" (c for center, g for goalie etc.)")
		results.append("To Use the Hand Filter add -HAND followed directly by \"l\" or \"r\"")
		results.append("\n")
		results.append("To Use the Less Than Or Equal to Age Filter add -AGE followed directly by \"the maximum age\"")
		results.append("To Use the Greater Than Or Equal to Age Filter add +AGE followed directly by \"the minimum age\"")
		results.append("\n")
		results.append("To Use the Less Than Or Equal to Height Filter add -HEIGHT followed directly by \"the maximum height\"")
		results.append("To Use the Greater Than Or Equal to Height Filter add +HEIGHT followed directly by \"the minimum height\"")
		results.append("\n")
		results.append("To Use the Less Than Or Equal to Weight Filter add -WEIGHT followed directly by \"the maximum weight\"")
		results.append("To Use the Greater Than Or Equal to Weight Filter add +WEIGHT followed directly by \"the minimum weight\"")
		results.append("\n")
		results.append("To Use the Less Than Or Equal to Rank Filter add -MAX-RANK followed directly by \"the maximum rank\"")
		results.append("To Use the Greater Than Or Equal to Rank Filter add -MIN-RANK followed directly by \"the minimum rank\"")
		results.append("\n")
		results.append("To Show A Single Player Info By NHL Player ID add -ID followed directly by \"the players nhl id\"")
		results.append("\n")
		results.append("*********************************************************************")
		results.append("\n")
	elif (useCountryCode or \
		useNegHeightFilter or \
		usePlusHeightFilter or \
		useNegAgeFilter or \
		usePlusAgeFilter or \
		useNegWeightFilter or \
		usePlusWeightFilter or \
		printOnlyRanked or \
		useNegRankFilter or \
		usePlusRankFilter or \
		useRankFilter or \
		printOnlyEligable or \
		usePositionFilter or \
		useHandFilter or \
		useLeagueFilter or \
		useTeamFilter) and not useIdFilter:
		results.append("\n")

		if len(countriesToSearchFor) > 0:
			results.append("Searching Birth Country Codes: " + str(countriesToSearchFor))

		results.append("Print Only Ranked Players: " + str(printOnlyRanked))
		results.append("Print Only Draft Eligable Players: " + str(printOnlyEligable))

		if usePositionFilter:
			results.append("Using Position Filter: " + str(positionFilter))

		if useHandFilter:
			results.append("Using Hand / Side Filter: " + str(handFilter))

		weightFilterEquality = "<=" if useNegWeightFilter else ">="

		if useWeightFilter:
			results.append("Using Weight Filter: " + weightFilterEquality + " " + str(weightFilter))

		heightFilterEquality = "<=" if useNegHeightFilter else ">="

		if useHeightFilter:
			results.append("Using Height Filter: " + heightFilterEquality + " " + str(heightFilter))

		ageFilterEquality = "<=" if useNegAgeFilter else ">="

		if useAgeFilter:
			results.append("Using Age Filter: " + ageFilterEquality + " " + str(ageFilter))

		rankFilterEquality = "<=" if useNegRankFilter else ">="

		if useRankFilter:
			results.append("Using Rank Filter: " + rankFilterEquality + " " + str(rankFilter))

		if len(leaguesFilter) > 0:
			results.append("Using Leagues Filter: " + str(leaguesFilter))

		if len(teamsFilter) > 0:
			results.append("Using Leagues Filter: " + str(teamsFilter))

		response = requests.get("https://statsapi.web.nhl.com/api/v1/draft/prospects")
		
		
		for p in response.json()['prospects']:
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
		processPlayers(sort(playerList, filterName=filterNameForSorting), results)		
	elif useIdFilter:
		nhlPlayerId = queryString[queryString.index('-ID')+1][0] if useIdFilter else ""

		results.append("\n")
		results.append("Using Player NHL ID Filter: " + nhlPlayerId)

		response = requests.get("https://statsapi.web.nhl.com/api/v1/draft/prospects/" + nhlPlayerId)

		json = response.json()['prospects']
		for p in json:
			newPlayer = Player(p=p)
			playerList.append(newPlayer)

		processPlayers(playerList, results)

	return results	