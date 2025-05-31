from utils import convert_height, calculateAge

def filterOne(useCountryCode, p, countriesToSearchFor):
	if useCountryCode == False or ('birthCountry' in p and p['birthCountry'] in countriesToSearchFor):
		return True
	return False

def filterTwo(useRankFilter, p, rankFilter, useNegRankFilter):	
	# If rank filtering is disabled, always return True
	if useRankFilter == False and useNegRankFilter == False:
		return True
	
	# If rank filtering is enabled, check if player has rank data
	if 'ranks' not in p or not p['ranks']:
		return False
	
	# Check rank conditions
	if useNegRankFilter:
		if 'midterm' in p['ranks']:
			return int(p['ranks']['midterm']) <= int(rankFilter)
		elif 'finalrank' in p['ranks']:
			return int(p['ranks']['finalrank']) <= int(rankFilter)
	else:
		if 'midterm' in p['ranks']:
			return int(p['ranks']['midterm']) >= int(rankFilter)
		elif 'finalrank' in p['ranks']:
			return int(p['ranks']['finalrank']) >= int(rankFilter)
	
	return False

def filterThree(printOnlyEligable, p):
	if printOnlyEligable == False or ('draftStatus' in p and "Elig" in p['draftStatus']):
		return True
	return False

def filterFour(usePositionFilter, positionFilter, p):
	if (usePositionFilter == False or (p['primaryPosition']['abbreviation'] in positionFilter)):
		return True
	return False

def filterFive(useHandFilter, p, handFilter):
	if useHandFilter == False or 'shootsCatches' in p and (handFilter in p['shootsCatches']):
		return True
	return False

def filterSix(useHeightFilter, p, heightFilter, useNegHeightFilter):
	if useHeightFilter == False:
		return True
	
	if 'height' not in p or not p['height']:
		return False
	
	player_height = convert_height(p['height'])
	filter_height = convert_height(heightFilter)
	
	if useNegHeightFilter:
		return player_height <= filter_height
	else:
		return player_height >= filter_height

def filterSeven(useWeightFilter, p, weightFilter, useNegWeightFilter):
	if useWeightFilter == False:
		return True
	
	if 'weight' not in p or not p['weight']:
		return False
	
	player_weight = int(p['weight'])
	filter_weight = int(weightFilter)
	
	if useNegWeightFilter:
		return player_weight <= filter_weight
	else:
		return player_weight >= filter_weight

def filterEight(useAgeFilter, p, ageFilter, useNegAgeFilter):
	if useAgeFilter == False:
		return True
	
	if 'birthDate' not in p or not p['birthDate']:
		return False
	
	player_age = int(calculateAge(p['birthDate']))
	filter_age = int(ageFilter)
	
	if useNegAgeFilter:
		return player_age <= filter_age
	else:
		return player_age >= filter_age

def filterNine(useLeagueFilter, p, leaguesFilter):
	if useLeagueFilter == False or ('amateurLeague' in p and \
		'name' in p['amateurLeague'] and \
		p['amateurLeague']['name'] in leaguesFilter):
		return True
	return False

def filterTen(useTeamFilter, p, teamsFilter):
	if useTeamFilter == False or ('amateurTeam' in p and \
			'name' in p['amateurTeam'] and \
			p['amateurTeam']['name'] in teamsFilter):
		return True
	return False

def all(p, 
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
		useWeightFilter,
		weightFilter, 
		useNegWeightFilter,
		useAgeFilter, 
		ageFilter, 
		useNegAgeFilter,
		useLeagueFilter,
		leaguesFilter,
		useTeamFilter, 
		teamsFilter):
			return filterOne(useCountryCode, p, countriesToSearchFor) and \
				filterTwo(useRankFilter, p, rankFilter, useNegRankFilter) and \
				filterThree(printOnlyEligable, p) and \
				filterFour(usePositionFilter, positionFilter, p) and \
				filterFive(useHandFilter, p, handFilter) and \
				filterSix(useHeightFilter, p, heightFilter, useNegHeightFilter) and \
				filterSeven(useWeightFilter, p, weightFilter, useNegWeightFilter) and \
				filterEight(useAgeFilter, p, ageFilter, useNegAgeFilter) and \
				filterNine(useLeagueFilter, p, leaguesFilter) and \
				filterTen(useTeamFilter, p, teamsFilter)