import { useEffect, useMemo, useState } from "react";
import axios from "axios";

export default function PlayerName(props) {
	const [info, setInfo] = useState(null);
	const [href, setHref] = useState("");
	const getInfo = async () => {
		const data = await fetch(href);
		const json = await data.json();
		const id = json[0].id
		const stats = await axios.get(`https://www.eliteprospects.com/ajax/player.stats.default?playerId=${id}`);
		const htmlMaybe = await stats.text();
		console.log("stats : " ,htmlMaybe);
		setInfo(htmlMaybe);
	};
	const getName = useMemo(() => {
		if (props?.playerData.includes("Player Full Name")) {
			const name = props.playerData.split(":")[1];
			const linkName = name.replace("%20", "+");
			setHref(`https://autocomplete.eliteprospects.com/all?q=${linkName}`);
			return (<>
				<button onClick={() => getInfo()}>
					Get Info
				</button>
				{name}
				<>
				info:
				{info}
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