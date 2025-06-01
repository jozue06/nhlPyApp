import { useMemo, useState, useCallback, SyntheticEvent } from "react";

const PlayerInfo = ({ playerData }: { playerData: any }) => {
  const [infoVisible, setInfoVisible] = useState<boolean>(false);
  const [infoLoaded, setInfoLoaded] = useState<boolean>(false);

  // Helper function to calculate age from birth date
  const calculateAge = (birthDate: string) => {
    if (!birthDate) return 0;
    const birth = new Date(birthDate);
    const now = new Date();
    let age = now.getFullYear() - birth.getFullYear();
    const monthDiff = now.getMonth() - birth.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && now.getDate() < birth.getDate())) {
      age--;
    }
    return age;
  };

  const toggleInfo = useCallback(async () => {
    const infoDiv = document.getElementById(
      `infos${playerData.fullName}`
    ) as HTMLDivElement;

    if (!infoLoaded) {
      try {
        const linkName = playerData.fullName.replace(" ", "+");
        const href = `https://autocomplete.eliteprospects.com/all?q=${linkName}`;
        const data = await fetch(href);
        const json = await data.json();

        if (!json || json.length === 0) {
          infoDiv.innerHTML =
            '<p style="color: #ff6b6b; padding: 10px;">No player information found</p>';
          setInfoLoaded(true);
          setInfoVisible(true);
          return;
        }

        const found =
          json.length === 1
            ? json[0]
            : json.find((e: any) => e.fullname === playerData.fullName);

        if (!found || !found.id) {
          infoDiv.innerHTML = `<p style="color: #ff6b6b; padding: 10px;">Player "${playerData.fullName.trim()}" not found.</p>`;
          setInfoLoaded(true);
          setInfoVisible(true);
          return;
        }

        const id = found.id;

        const iframe = document.createElement("iframe");
        iframe.src = `https://www.eliteprospects.com/ajax/player.stats.default?playerId=${id}`;
        iframe.id = `iframe-${playerData.fullName}`;
        iframe.style.minWidth = "70vw";
        iframe.style.backgroundColor = "darkgray";

        infoDiv.appendChild(iframe);
        setInfoLoaded(true);
        setInfoVisible(true);
      } catch {
        infoDiv.innerHTML =
          '<p style="color: #ff6b6b; padding: 10px;">Error loading player information. Please try again.</p>';
        setInfoLoaded(true);
        setInfoVisible(true);
      }
    } else {
      const iframe = document.getElementById(
        `iframe-${playerData.fullName}`
      ) as HTMLIFrameElement;
      const errorMessage = infoDiv.querySelector("p") as HTMLParagraphElement;

      if (iframe || errorMessage) {
        if (infoVisible) {
          if (iframe) {
            iframe.style.display = "none";
          }
          if (errorMessage) {
            errorMessage.style.display = "none";
          }
          setInfoVisible(false);
        } else {
          if (iframe) {
            iframe.style.display = "block";
          }
          if (errorMessage) {
            errorMessage.style.display = "block";
          }
          setInfoVisible(true);
        }
      }
    }
  }, [playerData.fullName, infoLoaded, infoVisible]);

  const playerDisplay = useMemo(() => {
    const age = calculateAge(playerData.birthDate);

    return (
      <div
        style={{
          margin: "10px 0",
          padding: "10px",
          border: "1px solid #ccc",
          borderRadius: "5px",
        }}
      >
        <div
          style={{ color: "#00ff00", fontWeight: "bold", marginBottom: "10px" }}
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

        <div style={{ color: "#00ff00" }}>Player NHL ID: {playerData.id}</div>
        <div style={{ color: "#00ff00" }}>
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
        <div style={{ color: "#00ff00" }}>
          Player Birth Date: {playerData.birthDate}
        </div>
        <div style={{ color: "#00ff00" }}>Player Current Age: {age}</div>
        <div style={{ color: "#00ff00" }}>
          Player Height: {playerData.height || "N/A"}
        </div>
        <div style={{ color: "#00ff00" }}>
          Player Weight: {playerData.weight ? `${playerData.weight}lbs` : "N/A"}
        </div>
        <div style={{ color: "#00ff00" }}>
          Player Birth Country: {playerData.birthCountry || "N/A"}
        </div>
        <div style={{ color: "#00ff00" }}>
          Player Position: {playerData.primaryPosition?.name || "N/A"}
        </div>

        {/* Handle shot/glove hand based on position */}
        {playerData.primaryPosition?.abbreviation === "G" ? (
          <div style={{ color: "#00ff00" }}>
            Player Glove Hand: {playerData.shootsCatches || "N/A"}
          </div>
        ) : (
          <div style={{ color: "#00ff00" }}>
            Player Shot Hand: {playerData.shootsCatches || "N/A"}
          </div>
        )}

        <div style={{ color: "#00ff00" }}>
          Player Draft Eligibility: {playerData.draftStatus || "N/A"}
        </div>
        <div style={{ color: "#00ff00" }}>
          Player Midterm Rank: not currently ranked
        </div>
        <div style={{ color: "#00ff00" }}>
          Player Final Rank: not currently ranked
        </div>

        <div id={`infos${playerData.fullName}`}></div>
      </div>
    );
  }, [playerData, infoVisible, infoLoaded, toggleInfo]);

  return <>{playerDisplay}</>;
};

export default PlayerInfo;
