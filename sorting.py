from utils import calculateAge


def sort(list, filterName):
    newList = []
    if filterName == "-NAME":
        newlist = sorted(list, key=lambda x: x.fullName)
    if filterName == "-HEIGHT":
        newlist = sorted(list, key=lambda x: x.height, reverse=True)
    if filterName == "+HEIGHT":
        newlist = sorted(list, key=lambda x: x.height)
    if filterName == "-AGE":
        newlist = sorted(
            list,
            key=lambda x: (
                calculateAge(x.birthDate)
                if hasattr(x, "birthDate") and x.birthDate
                else 0
            ),
            reverse=True,
        )
    if filterName == "+AGE":
        newlist = sorted(
            list,
            key=lambda x: (
                calculateAge(x.birthDate)
                if hasattr(x, "birthDate") and x.birthDate
                else 0
            ),
        )
    if filterName == "-WEIGHT":
        newlist = sorted(list, key=lambda x: x.weight, reverse=True)
    if filterName == "+WEIGHT":
        newlist = sorted(list, key=lambda x: x.weight)
    if filterName == "-RANK" or filterName == "-MAX-RANK" or filterName == "-MIN-RANK":
        # Handle ranking sorts - if no ranking data available, sort by name
        def get_rank(player):
            if hasattr(player, "ranks") and player.ranks:
                if "midterm" in player.ranks:
                    return int(player.ranks["midterm"])
                elif "finalrank" in player.ranks:
                    return int(player.ranks["finalrank"])
            # If no ranking data, put at end (high number) and sort by name as secondary
            return (9999, player.fullName)

        newlist = sorted(list, key=get_rank)

    return newlist
