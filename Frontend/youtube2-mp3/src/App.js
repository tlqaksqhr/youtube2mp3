import React, { Component } from 'react';
import './App.css';

import Nav from './Nav';
import SearchBox from './SearchBox'

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <Nav></Nav>
        </header>
        <div className="App-body">
          <SearchBox></SearchBox>
        </div>
      </div>
    );
  }
}

export default App;
