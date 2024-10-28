import './home.css';
import { Link } from 'react-router-dom';
import React, { useState, useEffect } from 'react';

const Home = () => {
    const [activeLink, setActiveLink] = useState('/');
    useEffect(() => {
        setActiveLink('/');
    }, []);
    return ( 
        <div>
            <br></br>
            <h1>Home</h1>
            <Link to="/travel/" className={activeLink === '/travel/' ? 'active' : ''} onClick={() => setActiveLink('/travel/')}>travel</Link>
        </div>
    );
}
 
export default Home;