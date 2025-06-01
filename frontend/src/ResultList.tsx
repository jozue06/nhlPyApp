import PlayerInfo from "./PlayerInfo";

interface ResultListProps {
  results: any[];
}

const ResultList = ({ results }: ResultListProps) => {
  // Count total players by counting "Player Full Name" occurrences
  const totalPlayers = results.filter(
    (line) => typeof line === "string" && line.includes("Player Full Name:")
  ).length;

  const listItems = results.map((res, i) => (
    <li key={res.toString() + i}>
      <PlayerInfo playerData={res} />
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
};

export default ResultList;
