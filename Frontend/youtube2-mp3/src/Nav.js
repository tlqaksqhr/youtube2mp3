import React, { Component } from 'react';
import './Nav.css'


class Nav extends Component{
    render() {
        return (
            <nav className="navigation-bar">
                <a href="#text-buttons"> Recommand </a>
                <a href="#text-buttons"> Home </a>
            </nav>
        );
    }
}

export default Nav;