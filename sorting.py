def sort(list, filterName):
	newList = []
	if filterName == "-NAME":
		newlist = sorted(list, key=lambda x: x.fullName)
	if filterName == "-HEIGHT":
		newlist = sorted(list, key=lambda x: x.height, reverse=True)
	if filterName == "+HEIGHT":
		newlist = sorted(list, key=lambda x: x.height)
	if filterName == "-AGE":
		newlist = sorted(list, key=lambda x: x.age, reverse=True)
	if filterName == "+AGE":
		newlist = sorted(list, key=lambda x: x.age)
	if filterName == "-WEIGHT":
		newlist = sorted(list, key=lambda x: x.weight, reverse=True)
	if filterName == "+WEIGHT":
		newlist = sorted(list, key=lambda x: x.weight)
	if filterName == "-TEAMS":
		newlist = sorted(list, key=lambda x: x.amateurTeam['name'])
	if filterName == "-LEAGUES":
		newlist = sorted(list, key=lambda x: x.amateurLeague['name'])
	if filterName == "-RANK":
		newlist = sorted(list, key=lambda x: x.ranks['midterm'])
		
	return newlist