import requests
from sorting import sort
from  processPlayers import processPlayers 
from playerClass import Player
from utils import convert_height, calculateAge

def processQueryString(queryString):
	partsToReturn = []
	parts = queryString.split(" ")
	
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


def process(queryString):
	results = []
	filterNameForSorting = "-NAME"
	queryString = processQueryString(queryString.upper())
	useIdFilter = '-ID' in queryString

	useCountryCode = '-CODES' in queryString
	countriesToSearchFor = queryString[queryString.index('-CODES')+1].upper() if useCountryCode else []

	useNegHeightFilter = '-HEIGHT' in queryString
	usePlusHeightFilter = '+HEIGHT' in queryString
	heightFilter = ""
	if useNegHeightFilter:
		heightFilter = queryString[queryString.index('-HEIGHT')+1]
		filterNameForSorting = "-HEIGHT"
	elif usePlusHeightFilter:
		heightFilter = queryString[queryString.index('+HEIGHT')+1]
		filterNameForSorting = "+HEIGHT"
	useHeightFilter = heightFilter != ""

	useNegAgeFilter = '-AGE' in queryString
	usePlusAgeFilter = '+AGE' in queryString
	ageFilter = ""
	if useNegAgeFilter:
		ageFilter = queryString[queryString.index('-AGE')+1]
		filterNameForSorting = "-AGE"
	elif usePlusAgeFilter:
		ageFilter = queryString[queryString.index('+AGE')+1]
		filterNameForSorting = "+AGE"

	useAgeFilter = ageFilter != ""

	useNegWeightFilter = '-WEIGHT' in queryString
	usePlusWeightFilter = '+WEIGHT' in queryString
	weightFilter = ""
	if useNegWeightFilter:
		weightFilter = queryString[queryString.index('-WEIGHT')+1]
		filterNameForSorting = "-WEIGHT"
	elif usePlusWeightFilter:
		weightFilter = queryString[queryString.index('+WEIGHT')+1]
		filterNameForSorting = "+WEIGHT"

	useWeightFilter = weightFilter != ""

	printOnlyRanked = '-RANKED' in queryString

	useNegRankFilter = '-MAX-RANK' in queryString
	usePlusRankFilter = '-MIN-RANK' in queryString
	rankFilter = "0"
	if useNegRankFilter:
		rankFilter = queryString[queryString.index('-MAX-RANK')+1]
		filterNameForSorting = "-MAX-RANK"
	elif usePlusRankFilter:
		rankFilter = queryString[queryString.index('-MIN-RANK')+1]
		filterNameForSorting = "-MIN-RANK"

	useRankFilter = rankFilter != ""

	if useRankFilter:
		printOnlyRanked = True
		filterNameForSorting = "-RANK"

	printAllInfo = '-ALL' in queryString
	printOnlyEligable = '-ELIG' in queryString

	usePositionFilter = '-POS' in queryString
	positionFilter = queryString[queryString.index('-POS')+1].upper() if usePositionFilter else "";

	useHandFilter = '-HAND' in queryString
	handFilter = queryString[queryString.index('-HAND')+1].upper() if useHandFilter else "";

	useLeagueFilter = '-LEAGUES' in queryString
	leaguesFilter = queryString[queryString.index('-LEAGUES')+1] if useLeagueFilter else [];

	if useLeagueFilter:
		filterNameForSorting = "-LEAGUES"

	useTeamFilter = '-TEAMS' in queryString
	teamsFilter = queryString[queryString.index('-TEAMS')+1].upper() if useTeamFilter else [];
	if useTeamFilter:
		filterNameForSorting = "-TEAMS"

	if "-H" in queryString or "-h" in queryString:
		results.append("\n")
		results.append("****************************THE HELP MENU****************************")
		results.append("\n")
		results.append("To Show Ranked Players Only add -RANKED")
		results.append("To Show Draft Eligable Players Only add -ELIG")
		results.append("To Show Full Player Info Object add -ALL")
		results.append("\n")
		results.append("To Use the Country Code Filter add -CODES followed directly \"codeOne,codeTwo\"")
		results.append("To Use the League Filter add -LEAGUES followed directly \"league one name,league two name\"")
		results.append("To Use the Team Filter add -TEAMS followed directly \"team one name,team two name\"")
		results.append("To Use the Position Filter add -POS followed directly \"c\" or \"g\" (c for center, g for goalie etc.)")
		results.append("To Use the Hand Filter add -HAND followed directly \"l\" or \"r\"")
		results.append("\n")
		results.append("To Use the Less Than Or Equal to Age Filter add -AGE followed directly \"the maximum age\"")
		results.append("To Use the Greater Than Or Equal to Age Filter add +AGE followed directly \"the minimum age\"")
		results.append("\n")
		results.append("To Use the Less Than Or Equal to Height Filter add -HEIGHT followed directly \"the maximum height\"")
		results.append("To Use the Greater Than Or Equal to Height Filter add +HEIGHT followed directly \"the minimum height\"")
		results.append("\n")
		results.append("To Use the Less Than Or Equal to Weight Filter add -WEIGHT followed directly \"the maximum weight\"")
		results.append("To Use the Greater Than Or Equal to Weight Filter add +WEIGHT followed directly \"the minimum weight\"")
		results.append("\n")
		results.append("To Use the Less Than Or Equal to Rank Filter add -MAX-RANK followed directly \"the maximum rank\"")
		results.append("To Use the Greater Than Or Equal to Rank Filter add -MIN-RANK followed directly \"the minimum rank\"")
		results.append("\n")
		results.append("To Show A Single Player Info By NHL Player ID add -ID followed directly \"the players nhl id\"")
		results.append("\n")
		results.append("*********************************************************************")
		results.append("\n")
	elif useCountryCode or useNegHeightFilter or usePlusHeightFilter or useNegAgeFilter or usePlusAgeFilter or useNegWeightFilter or usePlusWeightFilter or printOnlyRanked or useNegRankFilter or usePlusRankFilter or useRankFilter or printAllInfo or printOnlyEligable or usePositionFilter or useHandFilter or useLeagueFilter or useTeamFilter:
		results.append("\n")

		if len(countriesToSearchFor) > 0:
			results.append("Searching Birth Country Codes: " + countriesToSearchFor)

		results.append("Print All Player Info: " + str(printAllInfo))
		results.append("Print Only Ranked Players: " + str(printOnlyRanked))
		results.append("Print Only Draft Eligable Players: " + str(printOnlyEligable))

		if usePositionFilter:
			results.append("Using Position Filter: " + positionFilter)

		if useHandFilter:
			results.append("Using Hand / Side Filter: " + handFilter)	

		weightFilterEquality = "<=" if useNegWeightFilter else ">="

		if useWeightFilter:
			results.append("Using Weight Filter: " + weightFilterEquality + " " + weightFilter)	

		heightFilterEquality = "<=" if useNegHeightFilter else ">="

		if useHeightFilter:
			results.append("Using Height Filter: " + heightFilterEquality + " " + heightFilter)	

		ageFilterEquality = "<=" if useNegAgeFilter else ">="

		if useAgeFilter:
			results.append("Using Age Filter: " + ageFilterEquality + " " + ageFilter)

		rankFilterEquality = "<=" if useNegRankFilter else ">="

		if useRankFilter:
			results.append("Using Rank Filter: " + rankFilterEquality + " " + rankFilter)	

		if len(leaguesFilter) > 0:
			results.append("Using Leagues Filter: " + str(leaguesFilter))

		if len(teamsFilter) > 0:
			results.append("Using Leagues Filter: " + str(teamsFilter))

		response = requests.get("https://statsapi.web.nhl.com/api/v1/draft/prospects")

		index = 0;
		playerList = []
		for p in response.json()['prospects']:
			if useCountryCode == False or ('birthCountry' in p and p['birthCountry'] in countriesToSearchFor):
				if useRankFilter == False or ('finalrank' in p['ranks'] and int(p['finalrank']['midterm']) <= int(rankFilter)) if useNegRankFilter else ('finalrank' in p['ranks'] and int(p['finalrank']['midterm']) >= int(rankFilter)) or ('midterm' in p['ranks'] and int(p['ranks']['midterm']) <= int(rankFilter)) if useNegRankFilter else ('midterm' in p['ranks'] and int(p['ranks']['midterm']) >= int(rankFilter)):
					if printOnlyEligable == False or ('draftStatus' in p and "Elig" in p['draftStatus']):
						if usePositionFilter == False or (positionFilter in p['primaryPosition']['abbreviation']):
							if useHandFilter == False or 'shootsCatches' in p and (handFilter in p['shootsCatches']):
								if useHeightFilter == False or 'height' in p and (convert_height(p['height']) <= convert_height(heightFilter) if useNegHeightFilter else convert_height(p['height']) >= convert_height(heightFilter)):
									if useWeightFilter == False or 'weight' in p and (int(p['weight']) <= int(weightFilter) if useNegWeightFilter else int(p['weight']) >= int(weightFilter)):
										if useAgeFilter == False or (int(calculateAge(p['birthDate'])) <= int(ageFilter) if useNegAgeFilter else int(calculateAge(p['birthDate'])) >= int(ageFilter)):
											if useLeagueFilter == False or ('amateurLeague' in p and 'name' in p['amateurLeague'] and p['amateurLeague']['name'] in leaguesFilter):
												if useTeamFilter == False or ('amateurTeam' in p and 'name' in p['amateurTeam'] and p['amateurTeam']['name'] in teamsFilter):
													index += 1
													if printAllInfo:
														results.append("#" + str(index))
														results.append("Player Current Age: " + str(calculateAge(p['birthDate'])))
														results.append("Full Player: " + json.dumps(p, indent=4))
													else:
														newPlayer = Player(p=p, index=index)
														playerList.append(newPlayer)
														
	# elif useIdFilter:
		# nhlPlayerId = queryString[queryString.index('-ID')+1].upper() if useIdFilter else "";
		# results.append("\n")
		# results.append("Using Player NHL ID Filter: " + nhlPlayerId)
		# response = requests.get("https://statsapi.web.nhl.com/api/v1/draft/prospects/" + nhlPlayerId)
		# json = response.json()['prospects']
		# for p in json:
		# 	results.append("\n***********************************************\n")
		# 	results.append("Player NHL ID: " + str(p['id']))
		# 	results.append("Player Full Name: " + p['fullName'])
		# 	results.append("Player Birth Date: " + p['birthDate'])
		# 	results.append("Player Current Age: " + str(calculateAge(p['birthDate'])))
		# 	if 'height' in p:
		# 		results.append("Player Height: " + p['height'])
		# 	else:
		# 		results.append("Player Height: N/A")
		# 	if 'weight'	in p:
		# 		results.append("Player Weight: " + str(p['weight']) + "lbs")
		# 	else:
		# 		results.append("Player Weight: N/A")
		# 	if 'birthCountry' in p:
		# 		results.append("Player Birth Country: " + p['birthCountry'])
		# 	else: 
		# 		results.append("Player Birth Country: N/A")

		# 	results.append("Player Position: " + p['primaryPosition']['name'])
		# 	if 'G' in p['primaryPosition']['abbreviation']:
		# 		if 'shootsCatches' in p:
		# 			results.append("Player Glove Hand: " + p['shootsCatches'])
		# 		else:
		# 			results.append("Player Glove Hand: N/A")
		# 	else:
		# 		if 'shootsCatches' in p:
		# 			results.append("Player Shot Hand: " + p['shootsCatches'])	
		# 		else:
		# 			results.append("Player Shot Hand: N/A")
		# 	results.append("Player Draft Eligibility: " + p['draftStatus'])
		# 	if 'name' in p['amateurTeam']:
		# 		results.append("Player Amateur Team: " + p['amateurTeam']['name'])
		# 	if 'amateurLeague' in p and 'name' in p['amateurLeague']:
		# 		results.append("Player Amateur League: " + p['amateurLeague']['name'])
		# 	if 'midterm' in p['ranks']:
		# 		results.append("Player midterm Rank: " + str(p['ranks']['midterm']))
		# 	if 'finalrank' in p['ranks']:
		# 		results.append("Player finalrank Rank: " + str(p['ranks']['finalrank']))
		
		processPlayers(sort(playerList, filterName=filterNameForSorting), results)
	return results