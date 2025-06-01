from utils import calculateAge


def processPlayers(playerList, stringListResults):
    index = 1
    for p in playerList:
        topline = (
            "# " + str(index) + " \n***********************************************\n"
        )
        stringListResults.append(topline)
        stringListResults.append("Player NHL ID: " + str(p.id))
        stringListResults.append("Player Full Name: " + p.fullName)
        # Add headshot URL if available
        if hasattr(p, "headshot") and p.headshot:
            stringListResults.append("Player Headshot: " + p.headshot)
        else:
            stringListResults.append("Player Headshot: N/A")
        stringListResults.append("Player Birth Date: " + p.birthDate)
        stringListResults.append(
            "Player Current Age: " + str(calculateAge(p.birthDate))
        )
        if p.height:
            stringListResults.append("Player Height: " + p.height)
        else:
            stringListResults.append("Player Height: N/A")
        if p.weight:
            stringListResults.append("Player Weight: " + str(p.weight) + "lbs")
        else:
            stringListResults.append("Player Weight: N/A")

        if p.birthCountry:
            stringListResults.append("Player Birth Country: " + p.birthCountry)
        else:
            stringListResults.append("Player Birth Country: N/A")
        stringListResults.append("Player Position: " + p.primaryPosition["name"])
        if p.primaryPosition["abbreviation"] == "G":
            if p.shootsCatches:
                stringListResults.append("Player Glove Hand: " + p.shootsCatches)
            else:
                stringListResults.append("Player Glove Hand: N/A")
        else:
            if p.shootsCatches:
                stringListResults.append("Player Shot Hand: " + p.shootsCatches)
            else:
                stringListResults.append("Player Shot Hand: N/A")
        stringListResults.append("Player Draft Eligibility: " + p.draftStatus)

        # Always show ranking information
        if hasattr(p, "ranks") and p.ranks:
            if "midterm" in p.ranks:
                stringListResults.append(
                    "Player Midterm Rank: " + str(p.ranks["midterm"])
                )
            else:
                stringListResults.append("Player Midterm Rank: not currently ranked")

            if "finalrank" in p.ranks:
                stringListResults.append(
                    "Player Final Rank: " + str(p.ranks["finalrank"])
                )
            else:
                stringListResults.append("Player Final Rank: not currently ranked")
        else:
            stringListResults.append("Player Midterm Rank: not currently ranked")
            stringListResults.append("Player Final Rank: not currently ranked")

        index += 1


def processPlayersToJSON(playerList):
    """Convert player list to JSON format for React frontend"""
    results = []

    for p in playerList:
        player_data = {
            "id": str(p.id) if hasattr(p, 'id') and p.id else "",
            "fullName": p.fullName if hasattr(p, 'fullName') and p.fullName else "",
            "birthDate": p.birthDate if hasattr(p, 'birthDate') and p.birthDate else "",
            "height": p.height if hasattr(p, 'height') and p.height else "",
            "weight": p.weight if hasattr(p, 'weight') and p.weight else 0,
            "birthCountry": p.birthCountry if hasattr(p, 'birthCountry') and p.birthCountry else "",
            "headshot": p.headshot if hasattr(p, 'headshot') and p.headshot else "",
            "primaryPosition": {
                "name": p.primaryPosition.get("name", "") if hasattr(p, 'primaryPosition') and p.primaryPosition else "",
                "abbreviation": p.primaryPosition.get("abbreviation", "") if hasattr(p, 'primaryPosition') and p.primaryPosition else ""
            },
            "shootsCatches": p.shootsCatches if hasattr(p, 'shootsCatches') and p.shootsCatches else "",
            "draftStatus": p.draftStatus if hasattr(p, 'draftStatus') and p.draftStatus else "",
            "ranks": p.ranks if hasattr(p, 'ranks') and p.ranks else {}
        }
        results.append(player_data)

    return results
