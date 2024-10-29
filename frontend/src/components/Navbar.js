import { Link } from 'react-router-dom';
import React, { useState, useEffect } from 'react';

const Navbar = (user) => {
    const [activeLink, setActiveLink] = useState('/');
    useEffect(() => {
        setActiveLink('/');
    }, []);

    return ( 
        <nav className="navbar">
            <h1>TIM</h1>
            <div className="links">
                <Link to="/" className={activeLink === '/' ? 'active' : ''} onClick={() => setActiveLink('/')}>Home</Link>
                {user === null ? (
                    <Link to="/user/" className={activeLink === '/user/' ? 'active' : ''} onClick={() => setActiveLink('/user/')}>Sign In</Link>
                ) : (
                    <Link to="/user/" className={activeLink === '/user/' ? 'active' : ''} onClick={() => setActiveLink('/user/')}>user</Link>
                )}     
            </div>
            
        </nav>
    );
}
 
export default Navbar;