import { Link } from 'react-router-dom';
import './Navbar.css';
import React, { useState, useEffect } from 'react';

const Navbar = () => {
    const [activeLink, setActiveLink] = useState('/');
    useEffect(() => {
        setActiveLink('/');
    }, []);

    return ( 
        <nav className="navbar">
            <h1>TIM</h1>
            <div className="links">
                <Link to="/" className={activeLink === '/' ? 'active' : ''} onClick={() => setActiveLink('/')}>Home</Link>   
                <Link to="/user/" className={activeLink === '/user/' ? 'active' : ''} onClick={() => setActiveLink('/user/')}>User</Link>      
            </div>
            
        </nav>
    );
}
 
export default Navbar;