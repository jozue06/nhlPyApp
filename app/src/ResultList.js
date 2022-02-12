export default function ResultsList(props) {
	const results = props.results;
	const listItems = results.map((res, i) =>
	  <li key={res.toString()+i}>
		{res}
	  </li>
	);
	return (
	  <ul>{listItems}</ul>
	);
  }