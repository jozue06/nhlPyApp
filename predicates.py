from utils import convert_height, calculateAge

def filterOne(useCountryCode, p, countriesToSearchFor):
	if useCountryCode == False or ('birthCountry' in p and p['birthCountry'] in countriesToSearchFor):
		return True
	return False

def filterTwo(useRankFilter, p, rankFilter, useNegRankFilter):	

	if useRankFilter == False or ('finalrank' in p['ranks'] and \
		int(p['finalrank']['midterm']) <= int(rankFilter)) if useNegRankFilter else \
			('finalrank' in p['ranks'] and \
				int(p['finalrank']['midterm']) >= int(rankFilter)) or ('midterm' in p['ranks'] and \
				int(p['ranks']['midterm']) <= int(rankFilter)) if useNegRankFilter else \
			('midterm' in p['ranks'] and int(p['ranks']['midterm']) >= int(rankFilter)):
		return True
	return False

def filterThree(printOnlyEligable, p):
	if printOnlyEligable == False or ('draftStatus' in p and "Elig" in p['draftStatus']):
		return True
	return False

def filterFour(usePositionFilter, positionFilter, p):
	if (usePositionFilter == False or (positionFilter in p['primaryPosition']['abbreviation'])):
		return True
	return False

def filterFive(useHandFilter, p, handFilter):
	if useHandFilter == False or 'shootsCatches' in p and (handFilter in p['shootsCatches']):
		return True
	return False

def filterSix(useHeightFilter, p, heightFilter, useNegHeightFilter):
	if useHeightFilter == False or 'height' in p and \
			(convert_height(p['height']) <= convert_height(heightFilter) if useNegHeightFilter else \
			convert_height(p['height']) >= convert_height(heightFilter)):
		return True
	return False

def filterSeven(useWeightFilter, p, weightFilter, useNegWeightFilter):
	if useWeightFilter == False or 'weight' in p and \
			(int(p['weight']) <= int(weightFilter) if useNegWeightFilter else \
			int(p['weight']) >= int(weightFilter)):
		return True
	return False

def filterEight(useAgeFilter, p, ageFilter, useNegAgeFilter):
	if useAgeFilter == False or (int(calculateAge(p['birthDate'])) <= int(ageFilter) if useNegAgeFilter else \
		int(calculateAge(p['birthDate'])) >= int(ageFilter)):
		return True
	return False

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
				filterSeven(useNegWeightFilter, p, weightFilter, useNegWeightFilter) and \
				filterEight(useAgeFilter, p, ageFilter, useNegAgeFilter) and \
				filterNine(useLeagueFilter, p, leaguesFilter) and \
				filterTen(useTeamFilter, p, teamsFilter)