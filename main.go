package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"strconv"
	"strings"
	"time"

	"github.com/gin-contrib/cors"
	"github.com/gin-contrib/static"
	"github.com/gin-gonic/gin"
)

// Player represents the structure of player data
type Player struct {
	ID              string     `json:"id"`
	FullName        string     `json:"fullName"`
	BirthDate       string     `json:"birthDate"`
	Height          string     `json:"height"`
	Weight          int        `json:"weight"`
	BirthCountry    string     `json:"birthCountry"`
	Headshot        string     `json:"headshot"`
	PrimaryPosition Position   `json:"primaryPosition"`
	ShootsCatches   string     `json:"shootsCatches"`
	DraftStatus     string     `json:"draftStatus"`
	Ranks           map[string]interface{} `json:"ranks"`
}

// Position represents the position information
type Position struct {
	Name         string `json:"name"`
	Abbreviation string `json:"abbreviation"`
}

// NHLAPIPlayer represents a player from the NHL API
type NHLAPIPlayer struct {
	ID                int                    `json:"id"`
	FirstName         map[string]string      `json:"firstName"`
	LastName          map[string]string      `json:"lastName"`
	BirthDate         string                 `json:"birthDate"`
	BirthCountry      string                 `json:"birthCountry"`
	HeightInInches    int                    `json:"heightInInches"`
	WeightInPounds    int                    `json:"weightInPounds"`
	PositionCode      string                 `json:"positionCode"`
	ShootsCatches     string                 `json:"shootsCatches"`
	Headshot          string                 `json:"headshot"`
}

// NHLAPIResponse represents the response from the NHL prospects API
type NHLAPIResponse struct {
	Forwards   []NHLAPIPlayer `json:"forwards"`
	Defensemen []NHLAPIPlayer `json:"defensemen"`
	Goalies    []NHLAPIPlayer `json:"goalies"`
}

// SearchRequest represents the incoming search request
type SearchRequest struct {
	QueryString string `json:"queryString"`
}

// HelpResponse represents a help message response
type HelpResponse struct {
	IsHelp   bool     `json:"isHelp"`
	Messages []string `json:"messages"`
}

// NHLTeams list for processing
var NHLTeams = []string{
	"ANA", "BOS", "BUF", "CGY", "CAR", "CHI", "COL", "CBJ",
	"DAL", "DET", "EDM", "FLA", "LAK", "MIN", "MTL", "NSH",
	"NJD", "NYI", "NYR", "OTT", "PHI", "PIT", "SJS", "SEA",
	"STL", "TBL", "TOR", "UTA", "VAN", "VGK", "WSH", "WPG",
}

func main() {
	// Set Gin mode
	if os.Getenv("GIN_MODE") == "" {
		gin.SetMode(gin.DebugMode)
	}

	r := gin.Default()

	// CORS configuration
	config := cors.DefaultConfig()
	config.AllowAllOrigins = true
	config.AllowMethods = []string{"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"}
	config.AllowHeaders = []string{"Origin", "Content-Length", "Content-Type", "Authorization"}
	r.Use(cors.New(config))

	// Serve static files from React build
	r.Use(static.Serve("/assets", static.LocalFile("./frontend/build/assets", false)))
	r.StaticFile("/favicon.ico", "./frontend/build/favicon.ico")

	// API routes
	api := r.Group("/api")
	{
		api.POST("/json/search", handleSearchJSON) // React frontend uses POST
		api.GET("/json/search", handleSearchGET)   // Add GET handler for browser testing
	}

	// Serve React app for all other routes
	r.GET("/react", func(c *gin.Context) {
		c.File("./frontend/build/index.html")
	})

	// Root route - serve React app
	r.GET("/", func(c *gin.Context) {
		c.File("./frontend/build/index.html")
	})

	// Fallback route for React routing
	r.NoRoute(func(c *gin.Context) {
		c.File("./frontend/build/index.html")
	})

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	log.Printf("Server starting on port %s", port)
	log.Fatal(r.Run(":" + port))
}

func handleSearchJSON(c *gin.Context) {
	var request SearchRequest
	if err := c.ShouldBindJSON(&request); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Parse the query filters
	filters := processQueryString(request.QueryString)

	// Check if it's a help request
	if filters.ShowHelp {
		helpResponse := HelpResponse{
			IsHelp:   true,
			Messages: generateHelpMessage(),
		}
		c.JSON(http.StatusOK, helpResponse)
		return
	}

	// Fetch real player data from NHL API
	allPlayers, err := fetchAllPlayers()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to fetch player data"})
		return
	}

	// Apply filters to the players
	results := applyFilters(allPlayers, filters)

	c.JSON(http.StatusOK, results)
}

func handleSearchGET(c *gin.Context) {
	// Handle GET requests for browser testing
	queryString := c.Query("q")

	// Parse the query filters
	filters := processQueryString(queryString)

	// Check if it's a help request
	if filters.ShowHelp {
		helpResponse := HelpResponse{
			IsHelp:   true,
			Messages: generateHelpMessage(),
		}
		c.JSON(http.StatusOK, helpResponse)
		return
	}

	// Fetch real player data from NHL API
	allPlayers, err := fetchAllPlayers()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to fetch player data"})
		return
	}

	// Apply filters to the players
	results := applyFilters(allPlayers, filters)

	c.JSON(http.StatusOK, results)
}

// fetchAllPlayers fetches real player data from the NHL API
func fetchAllPlayers() ([]Player, error) {
	var allPlayers []Player

	for _, teamAbbrev := range NHLTeams {
		url := fmt.Sprintf("https://api-web.nhle.com/v1/prospects/%s", teamAbbrev)

		resp, err := http.Get(url)
		if err != nil {
			log.Printf("Error fetching data for team %s: %v", teamAbbrev, err)
			continue
		}
		defer resp.Body.Close()

		if resp.StatusCode != http.StatusOK {
			log.Printf("Warning: Failed to get prospects for team %s (status: %d)", teamAbbrev, resp.StatusCode)
			continue
		}

		body, err := io.ReadAll(resp.Body)
		if err != nil {
			log.Printf("Error reading response for team %s: %v", teamAbbrev, err)
			continue
		}

		var apiResponse NHLAPIResponse
		if err := json.Unmarshal(body, &apiResponse); err != nil {
			log.Printf("Error parsing JSON for team %s: %v", teamAbbrev, err)
			continue
		}

		// Process forwards
		for _, player := range apiResponse.Forwards {
			convertedPlayer := convertAPIPlayerToPlayer(player)
			allPlayers = append(allPlayers, convertedPlayer)
		}

		// Process defensemen
		for _, player := range apiResponse.Defensemen {
			convertedPlayer := convertAPIPlayerToPlayer(player)
			allPlayers = append(allPlayers, convertedPlayer)
		}

		// Process goalies
		for _, player := range apiResponse.Goalies {
			convertedPlayer := convertAPIPlayerToPlayer(player)
			allPlayers = append(allPlayers, convertedPlayer)
		}
	}

	return allPlayers, nil
}

// convertAPIPlayerToPlayer converts NHL API player format to our Player format
func convertAPIPlayerToPlayer(apiPlayer NHLAPIPlayer) Player {
	// Get first and last name from the default locale
	firstName := ""
	lastName := ""
	if apiPlayer.FirstName != nil {
		firstName = apiPlayer.FirstName["default"]
	}
	if apiPlayer.LastName != nil {
		lastName = apiPlayer.LastName["default"]
	}
	fullName := strings.TrimSpace(firstName + " " + lastName)

	// Convert height from inches to feet'inches" format
	height := ""
	if apiPlayer.HeightInInches > 0 {
		feet := apiPlayer.HeightInInches / 12
		inches := apiPlayer.HeightInInches % 12
		height = fmt.Sprintf(`%d'%d"`, feet, inches)
	}

	// Convert position code to full position name
	positionName := ""
	switch apiPlayer.PositionCode {
	case "C":
		positionName = "Center"
	case "L":
		positionName = "Left Wing"
	case "R":
		positionName = "Right Wing"
	case "D":
		positionName = "Defenseman"
	case "G":
		positionName = "Goalie"
	default:
		positionName = apiPlayer.PositionCode
	}

	return Player{
		ID:           strconv.Itoa(apiPlayer.ID),
		FullName:     fullName,
		BirthDate:    apiPlayer.BirthDate,
		Height:       height,
		Weight:       apiPlayer.WeightInPounds,
		BirthCountry: apiPlayer.BirthCountry,
		Headshot:     apiPlayer.Headshot,
		PrimaryPosition: Position{
			Name:         positionName,
			Abbreviation: apiPlayer.PositionCode,
		},
		ShootsCatches: apiPlayer.ShootsCatches,
		DraftStatus:   "Eligible", // Default since API doesn't provide this
		Ranks:         make(map[string]interface{}),
	}
}

// Helper functions for the mock data processing
func convertHeightToInches(heightStr string) int {
	// Convert height format like 6'1" to inches
	if !strings.Contains(heightStr, "'") {
		return 0
	}

	parts := strings.Split(heightStr, "'")
	if len(parts) != 2 {
		return 0
	}

	feet, err := strconv.Atoi(parts[0])
	if err != nil {
		return 0
	}

	inchesStr := strings.Trim(parts[1], `"`)
	inches, err := strconv.Atoi(inchesStr)
	if err != nil {
		return 0
	}

	return feet*12 + inches
}

func calculateAge(birthDate string) int {
	if birthDate == "" {
		return 0
	}

	layout := "2006-01-02"
	birth, err := time.Parse(layout, birthDate)
	if err != nil {
		return 0
	}

	now := time.Now()
	age := now.Year() - birth.Year()

	if now.YearDay() < birth.YearDay() {
		age--
	}

	return age
}

// convertPlayersToStringFormat converts player objects to the string format expected by React frontend
func convertPlayersToStringFormat(players []Player) []string {
	var results []string

	for i, player := range players {
		// Add header
		topline := "# " + strconv.Itoa(i+1) + " \n***********************************************\n"
		results = append(results, topline)

		// Add player information in the format expected by React
		results = append(results, "Player NHL ID: " + player.ID)
		results = append(results, "Player Full Name: " + player.FullName)

		// Add headshot URL if available
		if player.Headshot != "" {
			results = append(results, "Player Headshot: " + player.Headshot)
		} else {
			results = append(results, "Player Headshot: N/A")
		}

		results = append(results, "Player Birth Date: " + player.BirthDate)
		results = append(results, "Player Current Age: " + strconv.Itoa(calculateAge(player.BirthDate)))

		if player.Height != "" {
			results = append(results, "Player Height: " + player.Height)
		} else {
			results = append(results, "Player Height: N/A")
		}

		if player.Weight > 0 {
			results = append(results, "Player Weight: " + strconv.Itoa(player.Weight) + "lbs")
		} else {
			results = append(results, "Player Weight: N/A")
		}

		if player.BirthCountry != "" {
			results = append(results, "Player Birth Country: " + player.BirthCountry)
		} else {
			results = append(results, "Player Birth Country: N/A")
		}

		results = append(results, "Player Position: " + player.PrimaryPosition.Name)

		// Handle shot/glove hand based on position
		if player.PrimaryPosition.Abbreviation == "G" {
			if player.ShootsCatches != "" {
				results = append(results, "Player Glove Hand: " + player.ShootsCatches)
			} else {
				results = append(results, "Player Glove Hand: N/A")
			}
		} else {
			if player.ShootsCatches != "" {
				results = append(results, "Player Shot Hand: " + player.ShootsCatches)
			} else {
				results = append(results, "Player Shot Hand: N/A")
			}
		}

		results = append(results, "Player Draft Eligibility: " + player.DraftStatus)

		// Add ranking information (simplified for now)
		results = append(results, "Player Midterm Rank: not currently ranked")
		results = append(results, "Player Final Rank: not currently ranked")
	}

	return results
}
