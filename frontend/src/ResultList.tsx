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

  // Handle array of players (JSON objects)
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
