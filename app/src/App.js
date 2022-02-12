import './App.css';
import React, { useEffect, useState } from 'react';
import { Form } from "./Form";

function App() {
  const [getMessage, setGetMessage] = useState({})

  // useEffect(() => {
  //   axios.get('http://localhost:8000/').then(response => {
  //     console.log("SUCCESS", response)
  //     setGetMessage(response)
  //   }).catch(error => {
  //     console.log(error)
  //   })

  // }, [])
  return (
    <div className="App">
      <Form />
    
    </div>
  );
}

export default App;