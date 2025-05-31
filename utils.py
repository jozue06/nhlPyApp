from datetime import date
def convert_height(height):
	if not height:
		return 0
	
	# Handle new format like "5'11\""
	if "'" in height and '"' in height:
		parts = height.replace('"', '').split("'")
		if len(parts) == 2:
			feet = int(parts[0]) if parts[0].isdigit() else 0
			inches = int(parts[1]) if parts[1].isdigit() else 0
			return feet * 12 + inches
	
	# Handle old format (just a number string)
	if isinstance(height, str) and height.isdigit():
		return int(height)
	
	# Handle numeric values
	if isinstance(height, (int, float)):
		return int(height)
	
	return 0

	
def calculateAge(birthDateString):
	birthParts = birthDateString.split("-")
	birthDate = date(int(birthParts[0]), int(birthParts[1]), int(birthParts[2]))
	today = date.today()
	age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))

	return age
