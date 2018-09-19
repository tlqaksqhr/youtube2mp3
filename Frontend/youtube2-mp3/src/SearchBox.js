import React, { Component } from 'react';
import Button from '@material-ui/core/Button';

import './SearchBox.css'


class SearchBox extends Component{
    render() {
        return (
        <div className="content-box">
            <div>
            <i className="fa fa-youtube-play fa-5x" />
                <h1>YOUTUBE 2 MP3</h1>
            </div>
            <form method="post">
                <input id="input" type="text" name="url" width="30em"/>         
                <div className="button-box">
                    <Button> Convert </Button>
                    <Button> Covert Recommand </Button>
                </div>
            </form>
        </div>
        );
    }
}

export default SearchBox;