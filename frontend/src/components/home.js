import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const Home = ({ user }) => {
    const [activeLink, setActiveLink] = useState('/');

    useEffect(() => {
        setActiveLink('/');
    }, []);

    return (
        <div>
            <br />
            <h1>Welcome to Travel Itinerary Manager! {user} </h1>
            <br />
            
            <h2>
                {user ? (
                    <Link
                        to="/travel/"
                        className={activeLink === '/travel/' ? 'active' : ''}
                        onClick={() => setActiveLink('/travel/')}
                    >
                        travel
                    </Link>
                ) : (
                    <div><Link
                        to="/signin/"
                        className={activeLink === '/signin/' ? 'active' : ''}
                        onClick={() => setActiveLink('/signin/')}
                    >SIGN IN</Link> to start planning your trip!</div>
                )}
            </h2>
        </div>
    );
};

export default Home;
