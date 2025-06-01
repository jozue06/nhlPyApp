import PlayerInfo from "./PlayerInfo";

const ResultList = ({ results }: { results: any }) => {
  // Handle help response
  if (results && typeof results === "object" && results.isHelp) {
    return (
      <div>
        <div
          style={{
            color: "#00ff00",
            padding: "10px",
            margin: "10px 0",
            fontWeight: "bold",
            textAlign: "center",
          }}
        >
          Help Information
        </div>
        <ul>
          {results.messages.map((message: string, index: number) => (
            <li key={index} style={{ color: "#00ff00", padding: "5px" }}>
              {message}
            </li>
          ))}
        </ul>
      </div>
    );
  }

  // Handle new JSON structure with players and filterInfo
  if (results && typeof results === "object" && results.players) {
    const players = results.players;
    const filterInfo = results.filterInfo || [];
    const totalPlayers = players.length;
    const error = results.error;

    const listItems = players.map((player: any, index: number) => (
      <li key={player.id + index}>
        <PlayerInfo playerData={player} />
      </li>
    ));

    return (
      <div>
        {/* Display filter information */}
        {filterInfo.length > 0 && (
          <div
            style={{
              color: "#ffff00",
              padding: "10px",
              margin: "10px 0",
              border: "1px solid #ffff00",
              borderRadius: "5px",
              backgroundColor: "#1a1a1a",
            }}
          >
            <div style={{ fontWeight: "bold", marginBottom: "5px" }}>
              Active Filters:
            </div>
            <ul style={{ margin: 0, paddingLeft: "20px" }}>
              {filterInfo.map((filter: string, index: number) => (
                <li key={index} style={{ marginBottom: "3px" }}>
                  {filter}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Display error if player not found */}
        {error && (
          <div
            style={{
              color: "#ff6b6b",
              padding: "10px",
              margin: "10px 0",
              fontWeight: "bold",
              textAlign: "center",
            }}
          >
            {error}
          </div>
        )}

        {/* Display total players count */}
        {totalPlayers > 0 && (
          <div
            style={{
              color: "#00ff00",
              padding: "10px",
              margin: "10px 0",
              fontWeight: "bold",
              textAlign: "center",
            }}
          >
            Total Players Found: {totalPlayers}
          </div>
        )}

        <ul>{listItems}</ul>
      </div>
    );
  }

  // Handle legacy array format (for backward compatibility)
  if (Array.isArray(results)) {
    const totalPlayers = results.length;

    const listItems = results.map((player: any, index: number) => (
      <li key={player.id + index}>
        <PlayerInfo playerData={player} />
      </li>
    ));

    return (
      <div>
        {totalPlayers > 0 && (
          <div
            style={{
              color: "#00ff00",
              padding: "10px",
              margin: "10px 0",
              fontWeight: "bold",
              textAlign: "center",
            }}
          >
            Total Players Found: {totalPlayers}
          </div>
        )}
        <ul>{listItems}</ul>
      </div>
    );
  }

  // Fallback for unexpected format
  return (
    <div style={{ color: "#ff6b6b", padding: "10px" }}>
      Unexpected data format received
    </div>
  );
};

export default ResultList;
