import axios from "axios";
import React, { useEffect, useState } from 'react';

export class Form extends React.Component {
	constructor(props) {
	  super(props);
	  this.state = {value: '', data: null };
  
	  this.handleChange = this.handleChange.bind(this);
	  this.handleSubmit = this.handleSubmit.bind(this);
	}
  
	handleChange(event) {
	  this.setState({value: event.target.value});
	}
  
	async handleSubmit(event) {
	  event.preventDefault();
	  try {
	 	const results = await axios.post("http://localhost:8000/search", {queryString: this.state.value})
		console.log('results?', results);
		 		 
		this.setState({ data: results.data })
		console.log('thisstata', this.state.data);
		
	  } catch (error) {
		  console.log('err?? ', error);
		  
	  }
	}
  
	render() {
	  return (
		<div className="input-wrapper">
        <form onSubmit={this.handleSubmit}>
          <textarea value={this.state.value} onChange={this.handleChange} name="queryString" className="terminal" autoFocus={true} rows="10" cols="100"></textarea>
          <input type="submit" value="Submit" />
        </form>
		<div style={{color: 'aqua'}}>
			{this.state.data ? 
          <h3>{this.state.data}</h3>
          : <h1>
			  
		  </h1>}
		</div>
      </div>
	  );
	}
  }