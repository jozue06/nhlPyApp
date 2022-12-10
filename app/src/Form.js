import axios from "axios";
import React from 'react';
import ResultList from "./ResultList"
export class Form extends React.Component {
	constructor(props) {
		super(props);
		this.state = {value: '', data: null, loading: false };

		this.handleChange = this.handleChange.bind(this);
		this.handleSubmit = this.handleSubmit.bind(this);
		this.onKeyPress = this.onKeyPress.bind(this);

	}

	onKeyPress(event){
		if(event.which === 13){
			this.handleSubmit(event)
			event.preventDefault();
		}
	}

	handleChange(event) {
		this.setState({ value: event.target.value });
	}

	async handleSubmit(event) {
		console.log("handle submit", )
		this.setState({ loading: true });
		event.preventDefault();
		try {
			const results = await axios.post("http://127.0.0.1:5000/api/json/search", { queryString: this.state.value })
			this.setState({ data: results.data })
			this.setState({ loading: false });
		} catch (error) {
			this.setState({ loading: false });
		}
	}

	render() {
		return (
			<div className="input-wrapper">
				<h6>This is the React.js version of the NHL Prospect Terminal App</h6>
				<form onSubmit={this.handleSubmit}>
					<textarea 
						id="textareainput"
						value={this.state.value} 
						onChange={this.handleChange} 
						onKeyPress={this.onKeyPress}
						name="queryString" 
						className="terminal" 
						autoFocus={true} 
						rows="10" 
						cols="100" 
					/>
					{this.state.loading ?
					<button 
						type="submit" 
						disabled={true}
					>submit</button> : 
					<button 
						type="submit" 
					>submit</button>}
				</form>

				<div style={{color: 'aqua'}}>
					{this.state.data ? 
						<ResultList results={this.state.data} />
					: <h1>

					</h1>}
				</div>
			</div>
		);
	}
}