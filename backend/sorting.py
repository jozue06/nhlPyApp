from utils import calculateAge


def sort(list, filterName):
    newList = list  # Default to original list

    if filterName == "-NAME":
        newList = sorted(list, key=lambda x: x.fullName)
    elif filterName == "-HEIGHT":
        newList = sorted(list, key=lambda x: x.height, reverse=True)
    elif filterName == "+HEIGHT":
        newList = sorted(list, key=lambda x: x.height)
    elif filterName == "-AGE":
        newList = sorted(
            list,
            key=lambda x: (
                calculateAge(x.birthDate)
                if hasattr(x, "birthDate") and x.birthDate
                else 0
            ),
            reverse=True,
        )
    elif filterName == "+AGE":
        newList = sorted(
            list,
            key=lambda x: (
                calculateAge(x.birthDate)
                if hasattr(x, "birthDate") and x.birthDate
                else 0
            ),
        )
    elif filterName == "-WEIGHT":
        newList = sorted(list, key=lambda x: x.weight, reverse=True)
    elif filterName == "+WEIGHT":
        newList = sorted(list, key=lambda x: x.weight)
    elif filterName == "-RANK" or filterName == "-MAX-RANK" or filterName == "-MIN-RANK":
        # Handle ranking sorts - if no ranking data available, sort by name
        def get_rank(player):
            if hasattr(player, "ranks") and player.ranks:
                if "midterm" in player.ranks:
                    return int(player.ranks["midterm"])
                elif "finalrank" in player.ranks:
                    return int(player.ranks["finalrank"])
            # If no ranking data, put at end (high number) and sort by name as secondary
            return (9999, player.fullName)

        newList = sorted(list, key=get_rank)

    return newList
