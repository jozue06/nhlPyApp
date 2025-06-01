from utils import calculateAge


def processPlayersToJSON(playerList):
    """Convert player list to JSON format for frontend"""
    results = []

    for p in playerList:
        # Calculate age if birth date is available
        age = calculateAge(p.birthDate) if hasattr(p, 'birthDate') and p.birthDate else "N/A"

        player_data = {
            "id": str(p.id) if hasattr(p, 'id') and p.id else "",
            "fullName": p.fullName if hasattr(p, 'fullName') and p.fullName else "",
            "firstName": p.firstName if hasattr(p, 'firstName') and p.firstName else "",
            "lastName": p.lastName if hasattr(p, 'lastName') and p.lastName else "",
            "birthDate": p.birthDate if hasattr(p, 'birthDate') and p.birthDate else "",
            "age": age,
            "height": p.height if hasattr(p, 'height') and p.height else "",
            "heightInInches": p.heightInInches if hasattr(p, 'heightInInches') and p.heightInInches else 0,
            "weight": p.weight if hasattr(p, 'weight') and p.weight else 0,
            "birthCountry": p.birthCountry if hasattr(p, 'birthCountry') and p.birthCountry else "",
            "headshot": p.headshot if hasattr(p, 'headshot') and p.headshot else "",
            "primaryPosition": {
                "name": p.primaryPosition.get("name", "") if hasattr(p, 'primaryPosition') and p.primaryPosition else "",
                "abbreviation": p.primaryPosition.get("abbreviation", "") if hasattr(p, 'primaryPosition') and p.primaryPosition else ""
            },
            "positionCode": p.positionCode if hasattr(p, 'positionCode') and p.positionCode else "",
            "shootsCatches": p.shootsCatches if hasattr(p, 'shootsCatches') and p.shootsCatches else "",
            "draftStatus": p.draftStatus if hasattr(p, 'draftStatus') and p.draftStatus else "",
            "ranks": p.ranks if hasattr(p, 'ranks') and p.ranks else {}
        }
        results.append(player_data)

    return results
