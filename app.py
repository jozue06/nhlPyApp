import requests
import json
import sys
from datetime import date

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
	queryString = request.args.get("queryString")

# useIdFilter = '-ID' in sys.argv[1:]
# def convert_height(height):
# 		return int(height.replace("'", "").replace("\"", "").replace(" ", ""))

	
# def calculateAge(birthDateString):
# 	birthParts = birthDateString.split("-")
# 	birthDate = date(int(birthParts[0]), int(birthParts[1]), int(birthParts[2]))
# 	today = date.today()
# 	age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))

# 	return age
# 	# 1;2m is dark grey
# 	# 1;3m is italic
# 	# 1;4m is underlined
# 	# 1;7m is highlighted
# 	# 1;8m is black
# 	# 1;9m is strikethrough
# 	# 1;31m is red text no background
# 	# 1;32m is green text no background
# 	# 1;33m is yellow text no background
# 	# 1;34m is blue text no background
# 	# 1;35m is purple text no background
# 	# 1;36m is teal text no background
# 	# 1;40m is regular text light grey background
# 	# 1;41m is regular text red background
# 	# 1;42m is regular text green background
# 	# 1;43m is regular text yellow background
# 	# 1;44m is regular text blue background
# 	# 1;45m is regular text purple background
# 	# 1;46m is regular text teal background
# 	# 1;47m is regular text white background
# 	# 1;100m is regular text grey background
# 	# 1;101m is regular text bright red background
# 	# 1;102m is regular text bright green background
# 	# 1;103m is regular text bright yellow background
# 	# 1;104m is regular text bright blue background
# 	# 1;105m is regular text bright purple background
# 	# 1;106m is regular text bright teal background

# if "-H" in sys.argv[1:] or "-h" in sys.argv[1:]:
# 	print("\n")
# 	print("\033[1;3m","\033[1;31m","****************************THE HELP MENU****************************")
# 	print("\n")
# 	print("\033[1;0m","\033[1;39m","     \u2022 To Show Ranked Players Only add","\033[1;4m", "-RANKED")
# 	print("\033[1;0m","\033[1;39m","     \u2022 To Show Draft Eligable Players Only add","\033[1;4m", "-ELIG")
# 	print("\033[1;0m","\033[1;39m","     \u2022 To Show Full Player Info Object add","\033[1;4m", "-ALL")
# 	print("\033[1;0m","\033[1;39m","\n")

# 	print("\033[1;0m","\033[1;39m","     \u2022 To Use the Country Code Filter add","\033[1;4m", "-CODES","\033[1;0m","\033[1;3m","followed directly by","\033[1;37m\"codeOne,codeTwo\"")
# 	print("\033[1;0m","\033[1;39m","     \u2022 To Use the League Filter add","\033[1;4m", "-LEAGUES","\033[1;0m","\033[1;3m","followed directly by","\033[1;37m\"league one name,league two name\"")
# 	print("\033[1;0m","\033[1;39m","     \u2022 To Use the Team Filter add","\033[1;4m", "-TEAMS","\033[1;0m","\033[1;3m","followed directly by","\033[1;37m\"team one name,team two name\"")
# 	print("\033[1;0m","\033[1;39m","     \u2022 To Use the Position Filter add","\033[1;4m", "-POS","\033[1;0m","\033[1;3m","followed directly by","\033[1;37m\"c\" or \"g\" (c for center, g for goalie etc.)")
# 	print("\033[1;0m","\033[1;39m","     \u2022 To Use the Hand Filter add","\033[1;4m", "-HAND","\033[1;0m","\033[1;3m","followed directly by","\033[1;37m\"l\" or \"r\"")
# 	print("\033[1;0m","\033[1;39m","\n")

# 	print("\033[1;0m","\033[1;39m","     \u2022 To Use the Less Than Or Equal to Age Filter add","\033[1;4m", "-AGE","\033[1;0m","\033[1;3m","followed directly by","\033[1;37m\"the maximum age\"") 
# 	print("\033[1;0m","\033[1;39m","     \u2022 To Use the Greater Than Or Equal to Age Filter add","\033[1;4m", "+AGE","\033[1;0m","\033[1;3m","followed directly by","\033[1;37m\"the minimum age\"") 
# 	print("\033[1;0m","\033[1;39m","\n")

# 	print("\033[1;0m","\033[1;39m","     \u2022 To Use the Less Than Or Equal to Height Filter add","\033[1;4m", "-HEIGHT","\033[1;0m","\033[1;3m","followed directly by","\033[1;37m\"the maximum height\"") 
# 	print("\033[1;0m","\033[1;39m","     \u2022 To Use the Greater Than Or Equal to Height Filter add","\033[1;4m", "+HEIGHT","\033[1;0m","\033[1;3m","followed directly by","\033[1;37m\"the minimum height\"") 
# 	print("\033[1;0m","\033[1;39m","\n")

# 	print("\033[1;0m","\033[1;39m","     \u2022 To Use the Less Than Or Equal to Weight Filter add","\033[1;4m", "-WEIGHT","\033[1;0m","\033[1;3m","followed directly by","\033[1;37m\"the maximum weight\"") 
# 	print("\033[1;0m","\033[1;39m","     \u2022 To Use the Greater Than Or Equal to Weight Filter add","\033[1;4m", "+WEIGHT","\033[1;0m","\033[1;3m","followed directly by","\033[1;37m\"the minimum weight\"") 
# 	print("\033[1;0m","\033[1;39m","\n")

# 	print("\033[1;0m","\033[1;39m","     \u2022 To Use the Less Than Or Equal to Rank Filter add","\033[1;4m", "-MAX-RANK","\033[1;0m","\033[1;3m","followed directly by","\033[1;37m\"the maximum rank\"") 
# 	print("\033[1;0m","\033[1;39m","     \u2022 To Use the Greater Than Or Equal to Rank Filter add","\033[1;4m", "-MIN-RANK","\033[1;0m","\033[1;3m","followed directly by","\033[1;37m\"the minimum rank\"") 
# 	print("\033[1;0m","\033[1;39m","\n")

# 	print("\033[1;0m","\033[1;39m","     \u2022 To Show A Single Player Info By NHL Player ID add","\033[1;4m", "-ID","\033[1;0m","\033[1;3m","followed directly by","\033[1;37m\"the players nhl id\"") 
# 	print("\n")
# 	print("\033[1;0m","\033[1;3m","\033[1;31m","*********************************************************************")
# 	print("\033[1;0m","\033[1;39m","\n")

# elif not useIdFilter:
# 	useCountryCode = '-CODES' in sys.argv[1:]
# 	countriesToSearchFor = sys.argv[1:][sys.argv[1:].index('-CODES')+1].upper() if useCountryCode else []

# 	useNegHeightFilter = '-HEIGHT' in sys.argv[1:]
# 	usePlusHeightFilter = '+HEIGHT' in sys.argv[1:]
# 	heightFilter = ""
# 	if useNegHeightFilter:
# 		heightFilter = sys.argv[1:][sys.argv[1:].index('-HEIGHT')+1]
# 	elif usePlusHeightFilter:
# 		heightFilter = sys.argv[1:][sys.argv[1:].index('+HEIGHT')+1]

# 	useHeightFilter = heightFilter != ""

# 	useNegAgeFilter = '-AGE' in sys.argv[1:]
# 	usePlusAgeFilter = '+AGE' in sys.argv[1:]
# 	ageFilter = ""
# 	if useNegAgeFilter:
# 		ageFilter = sys.argv[1:][sys.argv[1:].index('-AGE')+1]
# 	elif usePlusAgeFilter:
# 		ageFilter = sys.argv[1:][sys.argv[1:].index('+AGE')+1]

# 	useAgeFilter = ageFilter != ""

# 	useNegWeightFilter = '-WEIGHT' in sys.argv[1:]
# 	usePlusWeightFilter = '+WEIGHT' in sys.argv[1:]
# 	weightFilter = ""
# 	if useNegWeightFilter:
# 		weightFilter = sys.argv[1:][sys.argv[1:].index('-WEIGHT')+1]
# 	elif usePlusWeightFilter:
# 		weightFilter = sys.argv[1:][sys.argv[1:].index('+WEIGHT')+1]

# 	useWeightFilter = weightFilter != ""


# 	printOnlyRanked = '-RANKED' in sys.argv[1:]

# 	useNegRankFilter = '-MAX-RANK' in sys.argv[1:]
# 	usePlusRankFilter = '-MIN-RANK' in sys.argv[1:]
# 	rankFilter = ""
# 	if useNegRankFilter:
# 		rankFilter = sys.argv[1:][sys.argv[1:].index('-MAX-RANK')+1]
# 	elif usePlusRankFilter:
# 		rankFilter = sys.argv[1:][sys.argv[1:].index('-MIN-RANK')+1]

# 	useRankFilter = rankFilter != ""

# 	if useRankFilter:
# 		printOnlyRanked = True

# 	printAllInfo = '-ALL' in sys.argv[1:]
# 	printOnlyEligable = '-ELIG' in sys.argv[1:]

# 	usePositionFilter = '-POS' in sys.argv[1:]
# 	positionFilter = sys.argv[1:][sys.argv[1:].index('-POS')+1].upper() if usePositionFilter else "";

# 	useHandFilter = '-HAND' in sys.argv[1:]
# 	handFilter = sys.argv[1:][sys.argv[1:].index('-HAND')+1].upper() if useHandFilter else "";

# 	useLeagueFilter = '-LEAGUES' in sys.argv[1:]
# 	leaguesFilter = sys.argv[1:][sys.argv[1:].index('-LEAGUES')+1].upper() if useLeagueFilter else [];

# 	useTeamFilter = '-TEAMS' in sys.argv[1:]
# 	teamsFilter = sys.argv[1:][sys.argv[1:].index('-TEAMS')+1].upper() if useTeamFilter else [];

# 	print("\n")
# 	if len(countriesToSearchFor) > 0:
# 		print("Searching Birth Country Codes:", countriesToSearchFor)	
# 	print("Print All Player Info:", printAllInfo)
# 	print("Print Only Ranked Players:", printOnlyRanked)
# 	print("Print Only Draft Eligable Players:", printOnlyEligable)

# 	if usePositionFilter:
# 		print("Using Position Filter:", positionFilter)

# 	if useHandFilter:
# 		print("Using Hand / Side Filter:", handFilter)	

# 	weightFilterEquality = "<=" if useNegWeightFilter else ">="

# 	if useWeightFilter:
# 		print("Using Weight Filter:", weightFilterEquality , " ", weightFilter)	

# 	heightFilterEquality = "<=" if useNegHeightFilter else ">="

# 	if useHeightFilter:
# 		print("Using Height Filter:", heightFilterEquality , " ", heightFilter)	

# 	ageFilterEquality = "<=" if useNegAgeFilter else ">="

# 	if useAgeFilter:
# 		print("Using Age Filter:", ageFilterEquality , " ", ageFilter)

# 	rankFilterEquality = "<=" if useNegRankFilter else ">="

# 	if useRankFilter:
# 		print("Using Rank Filter:", rankFilterEquality , " ", rankFilter)	

# 	if len(leaguesFilter) > 0:
# 		print("Using Leagues Filter:", leaguesFilter)

# 	if len(teamsFilter) > 0:
# 		print("Using Leagues Filter:", teamsFilter)

# 	response = requests.get("https://statsapi.web.nhl.com/api/v1/draft/prospects")

# 	index = 0;

# 	for p in response.json()['prospects']:
# 		if useCountryCode == False or ('birthCountry' in p and p['birthCountry'] in countriesToSearchFor):
# 			if (printOnlyRanked == False or 'finalRank' in p['ranks']):
# 				if useRankFilter == False or (int(p['ranks']['finalRank']) <= int(rankFilter) if useNegRankFilter else int(p['ranks']['finalRank']) >= int(rankFilter)):
# 					if printOnlyEligable == False or ('draftStatus' in p and "Elig" in p['draftStatus']):
# 						if usePositionFilter == False or (positionFilter in p['primaryPosition']['abbreviation']):
# 							if useHandFilter == False or 'shootsCatches' in p and (handFilter in p['shootsCatches']):
# 								if useHeightFilter == False or 'height' in p and (convert_height(p['height']) <= convert_height(heightFilter) if useNegHeightFilter else convert_height(p['height']) >= convert_height(heightFilter)):
# 									if useWeightFilter == False or 'weight' in p and (int(p['weight']) <= int(weightFilter) if useNegWeightFilter else int(p['weight']) >= int(weightFilter)):
# 										if useAgeFilter == False or (int(calculateAge(p['birthDate'])) <= int(ageFilter) if useNegAgeFilter else int(calculateAge(p['birthDate'])) >= int(ageFilter)):
# 											if useLeagueFilter == False or ('amateurLeague' in p and 'name' in p['amateurLeague'] and p['amateurLeague']['name'] in leaguesFilter):
# 												if useTeamFilter == False or ('amateurTeam' in p and 'name' in p['amateurTeam'] and p['amateurTeam']['name'] in teamsFilter):
# 													print("\n***********************************************\n")
# 													index += 1
# 													if printAllInfo:
# 														print("#",index)
# 														print("Player Current Age:", calculateAge(p['birthDate']))
# 														print("Full Player:", json.dumps(p, indent=4))
# 													else:
# 														print("#",index)
# 														print("Player NHL ID:", p['id'])
# 														print("Player Full Name:", p['fullName'])
# 														print("Player Birth Date:", p['birthDate'])
# 														print("Player Current Age:", calculateAge(p['birthDate']))
# 														if 'height' in p:
# 															print("Player Height:", p['height'])
# 														else:
# 															print("Player Height: N/A")
# 														if 'weight'	in p:
# 															print("Player Weight:", p['weight'],"lbs")
# 														else:
# 															print("Player Weight: N/A")

# 														if 'birthCountry' in p:
# 															print("Player Birth Country:", p['birthCountry'])
# 														else: 
# 															print("Player Birth Country: N/A")
# 														print("Player Position:", p['primaryPosition']['name'])
# 														if 'G' in p['primaryPosition']['abbreviation']:
# 															if 'shootsCatches' in p:
# 																print("Player Glove Hand:", p['shootsCatches'])
# 															else:
# 																print("Player Glove Hand: N/A")
# 														else:
# 															if 'shootsCatches' in p:
# 																print("Player Shot Hand:", p['shootsCatches'])	
# 															else:
# 																print("Player Shot Hand: N/A")
# 														print("Player Draft Eligibility:", p['draftStatus'])
# 														if 'name' in p['amateurTeam']:
# 															print("Player Amateur Team:", p['amateurTeam']['name'])
# 														if 'amateurLeague' in p and 'name' in p['amateurLeague']:
# 															print("Player Amateur League:", p['amateurLeague']['name'])
# 														if 'finalRank' in p['ranks']:
# 															print("Player Rank:", p['ranks']['finalRank'])

# else:
# 	nhlPlayerId = sys.argv[1:][sys.argv[1:].index('-ID')+1].upper() if useIdFilter else "";
# 	print("\n")
# 	print("Using Player NHL ID Filter:",nhlPlayerId)
# 	response = requests.get("https://statsapi.web.nhl.com/api/v1/draft/prospects/"+nhlPlayerId)
# 	json = response.json()['prospects']
# 	for p in json:
# 		print("\n***********************************************\n")
# 		print("Player NHL ID:", p['id'])
# 		print("Player Full Name:", p['fullName'])
# 		print("Player Birth Date:", p['birthDate'])
# 		print("Player Current Age:", calculateAge(p['birthDate']))
# 		if 'height' in p:
# 			print("Player Height:", p['height'])
# 		else:
# 			print("Player Height: N/A")
# 		if 'weight'	in p:
# 			print("Player Weight:", p['weight'],"lbs")
# 		else:
# 			print("Player Weight: N/A")
# 		if 'birthCountry' in p:
# 			print("Player Birth Country:", p['birthCountry'])
# 		else: 
# 			print("Player Birth Country: N/A")

# 		print("Player Position:", p['primaryPosition']['name'])
# 		if 'G' in p['primaryPosition']['abbreviation']:
# 			if 'shootsCatches' in p:
# 				print("Player Glove Hand:", p['shootsCatches'])
# 			else:
# 				print("Player Glove Hand: N/A")
# 		else:
# 			if 'shootsCatches' in p:
# 				print("Player Shot Hand:", p['shootsCatches'])	
# 			else:
# 				print("Player Shot Hand: N/A")
# 		print("Player Draft Eligibility:", p['draftStatus'])
# 		if 'name' in p['amateurTeam']:
# 			print("Player Amateur Team:", p['amateurTeam']['name'])
# 		if 'amateurLeague' in p and 'name' in p['amateurLeague']:
# 			print("Player Amateur League:", p['amateurLeague']['name'])
# 		if 'finalRank' in p['ranks']:
# 			print("Player Rank:", p['ranks']['finalRank'])