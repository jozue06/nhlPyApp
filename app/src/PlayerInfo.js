import { useMemo, useState } from "react";

export default function PlayerName(props) {
	const [href, setHref] = useState("");
	const [pName, setPName] = useState("");
	const getInfo = async () => {
		const data = await fetch(href);
		const json = await data.json();
		
		const found = json.length == 1 ? json[0] : json.find((e) => e.fullname == pName)
		const id = found.id

		const iframe = document.createElement('iframe');
		iframe.src = `https://www.eliteprospects.com/ajax/player.stats.default?playerId=${id}`;
		document.body.appendChild(iframe);
		iframe.contentWindow.document.open();
		let theDive = document.getElementById(`infos${pName}`);
		iframe.id = pName;
		iframe.style.minWidth = "70vw";
		iframe.style.backgroundColor = "darkgray";
		theDive.appendChild(iframe);

	};
	const getName = useMemo(() => {
		if (props?.playerData.includes("Player Full Name")) {
			const name = props.playerData.split(":")[1];
			const linkName = name.replace("%20", "+");
			setHref(`https://autocomplete.eliteprospects.com/all?q=${linkName}`);
			setPName(name.trim());
			return (<>
				{props.playerData}
				<button onClick={() => getInfo()}>
					Get Info
				</button>
				<>
					<div id={`infos${pName}`}>
					</div>
				</>
			</>);
		} else {
			return (
				<>
					{props.playerData}
				</>
			)
		}
	}, [props]);
	return (
		<>
			{getName}
		</>
	);
  }