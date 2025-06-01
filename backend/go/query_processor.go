package main

import (
	"sort"
	"strconv"
	"strings"
)

// QueryFilters represents parsed query filters
type QueryFilters struct {
	UseIDFilter          bool
	UseCountryCode       bool
	CountriesToSearch    []string
	UseExcludeCountry    bool
	CountriesToExclude   []string
	UseHeightFilter      bool
	HeightFilterValue    string
	HeightFilterType     string // "+" or "-"
	UseAgeFilter         bool
	AgeFilterValue       string
	AgeFilterType        string // "+" or "-"
	UseWeightFilter      bool
	WeightFilterValue    string
	WeightFilterType     string // "+" or "-"
	PrintOnlyRanked      bool
	UseRankFilter        bool
	RankFilterValue      int
	RankFilterType       string // "MIN" or "MAX"
	PrintOnlyEligible    bool
	UsePositionFilter    bool
	PositionFilter       []string
	UseHandFilter        bool
	HandFilter           string
	ShowHelp             bool
	FilterForSorting     string
}

// processQueryString parses the query string into structured filters
func processQueryString(queryString string) QueryFilters {
	parts := strings.Fields(strings.TrimSpace(strings.ToUpper(queryString)))
	filters := QueryFilters{}

	for i, part := range parts {
		switch part {
		case "-H", "-h":
			filters.ShowHelp = true
		case "-ID":
			filters.UseIDFilter = true
		case "-CODES":
			if i+1 < len(parts) && !strings.HasPrefix(parts[i+1], "-") {
				filters.UseCountryCode = true
				filters.CountriesToSearch = strings.Split(strings.Trim(parts[i+1], `"`), ",")
			}
		case "-EXCLUDE-CODES":
			if i+1 < len(parts) && !strings.HasPrefix(parts[i+1], "-") {
				filters.UseExcludeCountry = true
				filters.CountriesToExclude = strings.Split(strings.Trim(parts[i+1], `"`), ",")
			}
		case "-HEIGHT":
			if i+1 < len(parts) && !strings.HasPrefix(parts[i+1], "-") {
				filters.UseHeightFilter = true
				filters.HeightFilterType = "-"
				filters.HeightFilterValue = parts[i+1]
				filters.FilterForSorting = "-HEIGHT"
			}
		case "+HEIGHT":
			if i+1 < len(parts) && !strings.HasPrefix(parts[i+1], "-") {
				filters.UseHeightFilter = true
				filters.HeightFilterType = "+"
				filters.HeightFilterValue = parts[i+1]
				filters.FilterForSorting = "+HEIGHT"
			}
		case "-AGE":
			if i+1 < len(parts) && !strings.HasPrefix(parts[i+1], "-") {
				filters.UseAgeFilter = true
				filters.AgeFilterType = "-"
				filters.AgeFilterValue = parts[i+1]
				filters.FilterForSorting = "-AGE"
			}
		case "+AGE":
			if i+1 < len(parts) && !strings.HasPrefix(parts[i+1], "-") {
				filters.UseAgeFilter = true
				filters.AgeFilterType = "+"
				filters.AgeFilterValue = parts[i+1]
				filters.FilterForSorting = "+AGE"
			}
		case "-WEIGHT":
			if i+1 < len(parts) && !strings.HasPrefix(parts[i+1], "-") {
				filters.UseWeightFilter = true
				filters.WeightFilterType = "-"
				filters.WeightFilterValue = parts[i+1]
				filters.FilterForSorting = "-WEIGHT"
			}
		case "+WEIGHT":
			if i+1 < len(parts) && !strings.HasPrefix(parts[i+1], "-") {
				filters.UseWeightFilter = true
				filters.WeightFilterType = "+"
				filters.WeightFilterValue = parts[i+1]
				filters.FilterForSorting = "+WEIGHT"
			}
		case "-RANKED":
			filters.PrintOnlyRanked = true
			filters.FilterForSorting = "-RANK"
		case "-MAX-RANK":
			if i+1 < len(parts) && !strings.HasPrefix(parts[i+1], "-") {
				if rankVal, err := strconv.Atoi(parts[i+1]); err == nil {
					filters.UseRankFilter = true
					filters.RankFilterType = "MAX"
					filters.RankFilterValue = rankVal
					filters.PrintOnlyRanked = true
					filters.FilterForSorting = "-MAX-RANK"
				}
			}
		case "-MIN-RANK":
			if i+1 < len(parts) && !strings.HasPrefix(parts[i+1], "-") {
				if rankVal, err := strconv.Atoi(parts[i+1]); err == nil {
					filters.UseRankFilter = true
					filters.RankFilterType = "MIN"
					filters.RankFilterValue = rankVal
					filters.PrintOnlyRanked = true
					filters.FilterForSorting = "-MIN-RANK"
				}
			}
		case "-ELIG":
			filters.PrintOnlyEligible = true
		case "-POS":
			if i+1 < len(parts) && !strings.HasPrefix(parts[i+1], "-") {
				filters.UsePositionFilter = true
				positions := strings.Split(strings.Trim(parts[i+1], `"`), ",")

				// Handle "F" for forwards
				for j, pos := range positions {
					if strings.ToUpper(pos) == "F" {
						positions[j] = "RW"
						positions = append(positions, "C", "LW")
						break
					}
				}
				filters.PositionFilter = positions
			}
		case "-HAND":
			if i+1 < len(parts) && !strings.HasPrefix(parts[i+1], "-") {
				filters.UseHandFilter = true
				filters.HandFilter = parts[i+1]
			}
		}
	}

	// Default sorting filter
	if filters.FilterForSorting == "" {
		filters.FilterForSorting = "-NAME"
	}

	return filters
}

// applyFilters applies all the filters to the player list
func applyFilters(players []Player, filters QueryFilters) []Player {
	if filters.ShowHelp {
		return []Player{} // Return empty for help
	}

	var filtered []Player

	for _, player := range players {
		if shouldIncludePlayer(player, filters) {
			filtered = append(filtered, player)
		}
	}

	// Sort the results
	sortPlayers(filtered, filters.FilterForSorting)

	return filtered
}

// shouldIncludePlayer checks if a player meets all filter criteria
func shouldIncludePlayer(player Player, filters QueryFilters) bool {
	// Country filter
	if filters.UseCountryCode {
		found := false
		for _, country := range filters.CountriesToSearch {
			if strings.EqualFold(player.BirthCountry, country) {
				found = true
				break
			}
		}
		if !found {
			return false
		}
	}

	// Exclude country filter
	if filters.UseExcludeCountry {
		for _, country := range filters.CountriesToExclude {
			if strings.EqualFold(player.BirthCountry, country) {
				return false
			}
		}
	}

	// Height filter
	if filters.UseHeightFilter {
		playerHeight := convertHeightToInches(player.Height)
		filterHeight, err := strconv.Atoi(filters.HeightFilterValue)
		if err == nil {
			if filters.HeightFilterType == "-" && playerHeight >= filterHeight {
				return false
			} else if filters.HeightFilterType == "+" && playerHeight <= filterHeight {
				return false
			}
		}
	}

	// Age filter
	if filters.UseAgeFilter {
		playerAge := calculateAge(player.BirthDate)
		filterAge, err := strconv.Atoi(filters.AgeFilterValue)
		if err == nil {
			if filters.AgeFilterType == "-" && playerAge >= filterAge {
				return false
			} else if filters.AgeFilterType == "+" && playerAge <= filterAge {
				return false
			}
		}
	}

	// Weight filter
	if filters.UseWeightFilter {
		filterWeight, err := strconv.Atoi(filters.WeightFilterValue)
		if err == nil {
			if filters.WeightFilterType == "-" && player.Weight >= filterWeight {
				return false
			} else if filters.WeightFilterType == "+" && player.Weight <= filterWeight {
				return false
			}
		}
	}

	// Position filter
	if filters.UsePositionFilter {
		found := false
		for _, pos := range filters.PositionFilter {
			if strings.EqualFold(player.PrimaryPosition.Abbreviation, pos) ||
				strings.EqualFold(player.PrimaryPosition.Name, pos) {
				found = true
				break
			}
		}
		if !found {
			return false
		}
	}

	// Hand filter
	if filters.UseHandFilter {
		if !strings.EqualFold(player.ShootsCatches, filters.HandFilter) {
			return false
		}
	}

	// Eligibility filter (simplified - all are eligible for now)
	if filters.PrintOnlyEligible {
		if player.DraftStatus != "Eligible" {
			return false
		}
	}

	// Rank filters (simplified - no ranking data for now)
	if filters.PrintOnlyRanked || filters.UseRankFilter {
		// For now, we'll allow all players through
		// In a real implementation, this would check ranking data
	}

	return true
}

// sortPlayers sorts the player list based on the specified criteria
func sortPlayers(players []Player, sortCriteria string) {
	switch sortCriteria {
	case "-NAME":
		sort.Slice(players, func(i, j int) bool {
			return players[i].FullName < players[j].FullName
		})
	case "-HEIGHT", "+HEIGHT":
		sort.Slice(players, func(i, j int) bool {
			heightI := convertHeightToInches(players[i].Height)
			heightJ := convertHeightToInches(players[j].Height)
			if sortCriteria == "-HEIGHT" {
				return heightI < heightJ
			}
			return heightI > heightJ
		})
	case "-AGE", "+AGE":
		sort.Slice(players, func(i, j int) bool {
			ageI := calculateAge(players[i].BirthDate)
			ageJ := calculateAge(players[j].BirthDate)
			if sortCriteria == "-AGE" {
				return ageI < ageJ
			}
			return ageI > ageJ
		})
	case "-WEIGHT", "+WEIGHT":
		sort.Slice(players, func(i, j int) bool {
			if sortCriteria == "-WEIGHT" {
				return players[i].Weight < players[j].Weight
			}
			return players[i].Weight > players[j].Weight
		})
	default:
		// Default to name sorting
		sort.Slice(players, func(i, j int) bool {
			return players[i].FullName < players[j].FullName
		})
	}
}

// generateHelpMessage returns the help message
func generateHelpMessage() []string {
	return []string{
		"",
		"****************************THE HELP MENU****************************",
		"",
		"To Show Ranked Players Only add -RANKED",
		"To Show Draft Eligible Players Only add -ELIG",
		"",
		"To Use the Country Code Filter add -CODES followed directly by \"codeOne,codeTwo\"",
		"To Exclude Country Codes add -EXCLUDE-CODES followed directly by \"codeOne,codeTwo\"",
		"",
		"To Use Height Filters:",
		"To Show Players UNDER a height add -HEIGHT followed directly by the height in inches",
		"To Show Players OVER a height add +HEIGHT followed directly by the height in inches",
		"",
		"To Use Age Filters:",
		"To Show Players UNDER an age add -AGE followed directly by the age",
		"To Show Players OVER an age add +AGE followed directly by the age",
		"",
		"To Use Weight Filters:",
		"To Show Players UNDER a weight add -WEIGHT followed directly by the weight in lbs",
		"To Show Players OVER a weight add +WEIGHT followed directly by the weight in lbs",
		"",
		"To Use Position Filter add -POS followed directly by \"positionOne,positionTwo\"",
		"Valid positions: C, LW, RW, D, G, F (F will show all forwards)",
		"",
		"To Use Hand Filter add -HAND followed directly by L or R",
		"",
		"To Use Rank Filters:",
		"To Show Players with a MAX rank add -MAX-RANK followed by the rank number",
		"To Show Players with a MIN rank add -MIN-RANK followed by the rank number",
		"",
		"***********************************************************************",
	}
}
