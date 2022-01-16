from datetime import date
def convert_height(height):
		return int(height.replace("' ").replace("\" ").replace("  "))

	
def calculateAge(birthDateString):
	birthParts = birthDateString.split("-")
	birthDate = date(int(birthParts[0]), int(birthParts[1]), int(birthParts[2]))
	today = date.today()
	age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))

	return age
