import axios from "axios";
import React, { useEffect, useState } from 'react';
import ResultList from "./ResultList"
export class Form extends React.Component {
	constructor(props) {
		super(props);
		this.state = {value: '', data: null, loading: false };

		this.handleChange = this.handleChange.bind(this);
		this.handleSubmit = this.handleSubmit.bind(this);
	}

	handleChange(event) {
		this.setState({ value: event.target.value });
	}

	async handleSubmit(event) {
		this.setState({ loading: true });
		event.preventDefault();
		try {
			const results = await axios.post("http://localhost:8000/api/json/search", { queryString: this.state.value })
			this.setState({ data: results.data })
			this.setState({ loading: false });
		} catch (error) {
			console.log('err?? ', error);
			this.setState({ loading: false });
		}
	}

	render() {
		return (
			<div className="input-wrapper">
				This is the React.js version of the NHL Prospect Terminal App
				<form onSubmit={this.handleSubmit}>
					<textarea 
						value={this.state.value} 
						onChange={this.handleChange} 
						name="queryString" 
						className="terminal" 
						autoFocus={true} 
						rows="10" 
						cols="100" 
					/>
					{this.state.loading ?
					<input 
						type="submit" 
						value="Submit" 
						disabled={true}
					/> : 
					<input 
						type="submit" 
						value="Submit" 
					/>}
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