import axios from 'axios';
import './App.css'
import { Component } from 'react';

class App extends Component {

  state = {
    details : [],
  }

  componentDidMount() {
    let data;

    axios.get("http://localhost:8000/api/races/")
    .then(res => {
      data = res.data;
      this.setState({
        details : data
      });
    })
    .catch(_ => {})
  }
  
  render() {
    console.log(this.state.details)
    return (
      <>
        <section id="center">
          <div className="hero">
            <h1>React Connection Test</h1>
          </div>
          {this.state.details.map((detail: any) => (
            <>
              <h2>{detail.title}</h2>
              <p>date ran: { detail.dateRan }</p>
              <p>location: { detail.location }</p>
              <p>distance: { detail.distanceKm }km</p>
              <p>src:      { detail.sourceUrl }</p>
            </>
            )
          )}
        </section>
      </>
    )
  }
}

export default App
