import { useMemo, useState, useCallback } from "react";

export default function PlayerName(props) {
  const [href, setHref] = useState("");
  const [pName, setPName] = useState("");
  const [infoVisible, setInfoVisible] = useState(false);
  const [infoLoaded, setInfoLoaded] = useState(false);

  const toggleInfo = useCallback(async () => {
    const infoDiv = document.getElementById(`infos${pName}`);

    if (!infoLoaded) {
      try {
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
          json.length == 1 ? json[0] : json.find(e => e.fullname == pName);

        if (!found || !found.id) {
          infoDiv.innerHTML = `<p style="color: #ff6b6b; padding: 10px;">Player "${pName.trim()}" not found.</p>`;
          setInfoLoaded(true);
          setInfoVisible(true);
          return;
        }

        const id = found.id;

        const iframe = document.createElement("iframe");
        iframe.src = `https://www.eliteprospects.com/ajax/player.stats.default?playerId=${id}`;
        iframe.id = `iframe-${pName}`;
        iframe.style.minWidth = "70vw";
        iframe.style.backgroundColor = "darkgray";

        infoDiv.appendChild(iframe);
        setInfoLoaded(true);
        setInfoVisible(true);
      } catch (error) {
        infoDiv.innerHTML =
          '<p style="color: #ff6b6b; padding: 10px;">Error loading player information. Please try again.</p>';
        setInfoLoaded(true);
        setInfoVisible(true);
      }
    } else {
      const iframe = document.getElementById(`iframe-${pName}`);
      const errorMessage = infoDiv.querySelector("p");

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
  }, [href, pName, infoLoaded, infoVisible]);

  const getName = useMemo(() => {
    if (
      props?.playerData.includes("Player Headshot:") &&
      props?.playerData.includes("http")
    ) {
      const headshotUrl = props.playerData.split("Player Headshot: ")[1];
      return (
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            margin: "10px 0",
          }}
        >
          <img
            src={headshotUrl}
            alt="Player headshot"
            style={{
              width: "100px",
              height: "100px",
              objectFit: "cover",
              borderRadius: "5px",
              border: "2px solid #00ff00",
            }}
            onError={e => {
              e.target.style.display = "none";
            }}
          />
        </div>
      );
    } else if (props?.playerData.includes("Player Full Name")) {
      const name = props.playerData.split(":")[1];
      const linkName = name.replace("%20", "+");
      setHref(`https://autocomplete.eliteprospects.com/all?q=${linkName}`);
      setPName(name.trim());
      return (
        <>
          {props.playerData}
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
          <>
            <div id={`infos${pName}`}></div>
          </>
        </>
      );
    } else {
      return <>{props.playerData}</>;
    }
  }, [props, infoVisible, infoLoaded, pName, toggleInfo]);
  return <>{getName}</>;
}
