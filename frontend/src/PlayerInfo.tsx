import { SyntheticEvent, useMemo, useCallback, useState } from "react";

const PlayerInfo = ({ playerData }: { playerData: any }) => {
  const [infoVisible, setInfoVisible] = useState(false);
  const [infoLoaded, setInfoLoaded] = useState(false);

  // Use age from API response instead of calculating it
  const age = playerData.age || "N/A";

  const toggleInfo = useCallback(async () => {
    const infoDiv = document.getElementById(
      `infos${playerData.fullName}`
    ) as HTMLDivElement;

    if (!infoLoaded) {
      try {
        const linkName = playerData.fullName.replace(/\s+/g, "+");
        const response = await fetch(
          `https://autocomplete.eliteprospects.com/all?q=${linkName}`
        );
        const json = await response.json();

        if (!json || json.length === 0) {
          infoDiv.innerHTML =
            '<p style="color: #ff6b6b; padding: 10px;">No player information found</p>';
        } else {
          const found =
            json.length === 1
              ? json[0]
              : json.find((e: any) => e.fullname === playerData.fullName);

          if (!found || !found.id) {
            infoDiv.innerHTML = `<p style="color: #ff6b6b; padding: 10px;">Player "${playerData.fullName}" not found.</p>`;
          } else {
            const iframe = document.createElement("iframe");
            iframe.src = `https://www.eliteprospects.com/ajax/player.stats.default?playerId=${found.id}`;
            iframe.style.minWidth = "70vw";
            iframe.style.backgroundColor = "darkgray";
            iframe.style.border = "1px solid #00ff00";
            infoDiv.appendChild(iframe);
          }
        }

        setInfoLoaded(true);
        setInfoVisible(true);
      } catch (error) {
        infoDiv.innerHTML =
          '<p style="color: #ff6b6b; padding: 10px;">Error loading player information. Please try again.</p>';
        setInfoLoaded(true);
        setInfoVisible(true);
      }
    } else {
      const iframe = infoDiv.querySelector("iframe");
      const errorMsg = infoDiv.querySelector("p");

      if (infoVisible) {
        if (iframe) {
          (iframe as HTMLElement).style.display = "none";
        }
        if (errorMsg) {
          (errorMsg as HTMLElement).style.display = "none";
        }
        setInfoVisible(false);
      } else {
        if (iframe) {
          (iframe as HTMLElement).style.display = "block";
        }
        if (errorMsg) {
          (errorMsg as HTMLElement).style.display = "block";
        }
        setInfoVisible(true);
      }
    }
  }, [playerData.fullName, infoLoaded, infoVisible]);

  const playerDisplay = useMemo(() => {
    return (
      <div
        style={{
          margin: "10px 0",
          padding: "10px",
        }}
      >
        <div
          style={{ color: "aqua", fontWeight: "bold", marginBottom: "10px" }}
        >
          Player Information
        </div>

        {/* Show headshot if available */}
        {playerData.headshot && (
          <div
            style={{
              display: "flex",
              justifyContent: "center",
              margin: "10px 0",
            }}
          >
            <img
              src={playerData.headshot}
              alt="Player headshot"
              style={{
                width: "100px",
                height: "100px",
                objectFit: "cover",
                borderRadius: "5px",
                border: "2px solid #00ff00",
              }}
              onError={(e: SyntheticEvent<HTMLImageElement>) => {
                (e.target as HTMLImageElement).style.display = "none";
              }}
            />
          </div>
        )}

        <div style={{ color: "aqua" }}>Player NHL ID: {playerData.id}</div>
        <div style={{ color: "aqua" }}>
          Player Full Name: {playerData.fullName}
          <button
            onClick={toggleInfo}
            style={{
              marginLeft: "10px",
              padding: "5px 10px",
              backgroundColor: infoVisible ? "#ff6b6b" : "#4ecdc4",
              color: "white",
              border: "none",
              borderRadius: "3px",
              cursor: "pointer",
            }}
          >
            {!infoLoaded ? "Get Info" : infoVisible ? "Hide Info" : "Show Info"}
          </button>
        </div>
        <div style={{ color: "aqua" }}>
          Player Birth Date: {playerData.birthDate}
        </div>
        <div style={{ color: "aqua" }}>Player Current Age: {age}</div>
        <div style={{ color: "aqua" }}>
          Player Height: {playerData.height || "N/A"}
        </div>
        <div style={{ color: "aqua" }}>
          Player Weight: {playerData.weight ? `${playerData.weight}lbs` : "N/A"}
        </div>
        <div style={{ color: "aqua" }}>
          Player Birth Country: {playerData.birthCountry || "N/A"}
        </div>
        <div style={{ color: "aqua" }}>
          Player Position: {playerData.primaryPosition?.name || "N/A"}
        </div>

        {/* Handle shot/glove hand based on position */}
        {playerData.primaryPosition?.abbreviation === "G" ? (
          <div style={{ color: "aqua" }}>
            Player Glove Hand: {playerData.shootsCatches || "N/A"}
          </div>
        ) : (
          <div style={{ color: "aqua" }}>
            Player Shot Hand: {playerData.shootsCatches || "N/A"}
          </div>
        )}

        <div style={{ color: "aqua" }}>
          Player Draft Eligibility: {playerData.draftStatus || "N/A"}
        </div>
        <div style={{ color: "aqua" }}>
          Player Midterm Rank: not currently ranked
        </div>
        <div style={{ color: "aqua" }}>
          Player Final Rank: not currently ranked
        </div>

        <div id={`infos${playerData.fullName}`}></div>

        {/* Add a horizontal line at the bottom of each player section */}
        <hr
          style={{
            border: "none",
            borderTop: "1px solid #444",
            margin: "15px 0",
          }}
        />
      </div>
    );
  }, [playerData, infoVisible, infoLoaded, toggleInfo, age]);

  return <>{playerDisplay}</>;
};

export default PlayerInfo;
