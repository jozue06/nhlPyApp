import PlayerInfo from "./PlayerInfo"
export default function ResultsList(props) {
	const results = props.results;
	const listItems = results.map((res, i) =>
	  <li key={res.toString()+i}>
		<PlayerInfo playerData={res} />
	  </li>
	);
	return (
	  <ul>{listItems}</ul>
	);
  }