import React, { Component } from 'react';
import './App.css';

import Nav from './Nav';
import Util from './util';

import Button from '@material-ui/core/Button';


const DOWNLOAD_STATE = {
  READY : 0,
  WAIT : 1,
  SUCCESS : 2,
  INVALID_PAGE : 3
}

class App extends Component {

  state = {
    DownloadPageState : DOWNLOAD_STATE.READY,
    Title: "",
    DownloadLink: "",
    YoutubeURL: ""
  }

  getYoutubeURL = (e) => {
    this.setState({"YoutubeURL" : e.target.value});
  }

  renderContentBox = () => {
    let statePage = this.state.DownloadPageState;

    switch(statePage)
    {
      case DOWNLOAD_STATE.READY:
        return (
          <form method="post">
            <input id="inputBox" type="text" name="url" width="30em" onChange={event => this.getYoutubeURL(event)}/>         
            <div className="button-box">
                <Button onClick={this.convertAction}> Convert </Button>
            </div>
          </form>
        );
      case DOWNLOAD_STATE.WAIT:
        return (
          <div>
            <h3>
              Download Proceed <i className="fa fa-youtube-play fa-1x" />
            </h3>
          </div>
        );
      case DOWNLOAD_STATE.SUCCESS:
        return (
          <div>
            <div>
              <h3>{this.state.Title}</h3>
            </div>
            <div className="button-box">
                <Button href={this.state.DownloadLink}>Download</Button>
            </div>
          </div>
        );
      default:
        return (
          <div>INVALID PAGE!</div>
        )
    }
  }

  async convertYoutubeVideo(url){
    this.setState({
      DownloadPageState: DOWNLOAD_STATE.WAIT
    });

    let req_param = {
      "url" : url
    };

    let response = await fetch(`http://localhost:8000/convert/`,{
      method: 'POST',
      mode: "cors",
      credentials: "same-origin",
      body: JSON.stringify(req_param),
    });

    console.log(await response.json());
  }

  async getDownloadLink(id){
    let response = await fetch(`http://localhost:8000/download_link/${id}`,{
      method: 'GET',
      mode: "cors",
      credentials: "same-origin",
    });

    let data = await response.json();

    if(data["status"] === "success")
    {
      this.setState({
        Title: data["title"],
        DownloadLink: data["download_url"],
        DownloadPageState: DOWNLOAD_STATE.SUCCESS
      });

      return true;
    }

    return false;
  }

  convertAction = async () => {

    let url = this.state.YoutubeURL;
    let id = Util.getVideoId(url);

    if(id !== "")
    {
      this.convertYoutubeVideo(url);
      
      let p = true;
      do{
        p = await this.getDownloadLink(id);
        console.log(p);
      }
      while(!p);
    }
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <Nav></Nav>
        </header>
        <div className="App-body">
          <div className="content-box">
            <div id="logo-box">
              <i className="fa fa-youtube-play fa-5x" />
              <h1>YOUTUBE 2 MP3</h1>
            </div>
            {this.renderContentBox()}
          </div>
        </div>
      </div>
    );
  }
}

export default App;
