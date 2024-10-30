import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const Home = ({ user }) => {
    const [activeLink, setActiveLink] = useState('/');
    const trip_ids = [1, 2, 3, 4];

    useEffect(() => {
        setActiveLink('/');
    }, []);

    return (
        <div>
            <br />
            {user ? (
            <div>
                <h1>Welcome, {user}! </h1>
                <br />
                <br />
                <br />
                {trip_ids.map((trip_id) => (
                    <h2 key={trip_id}>
                        <Link
                            to={`/trip/${trip_id}`}
                            className={activeLink === `/trip/${trip_id}` ? 'active' : ''}
                            onClick={() => setActiveLink(`/trip/${trip_id}`)}
                        >
                            Trip {trip_id}
                        </Link>
                    </h2>
                ))}
                <br />
                <br />
                <br />
                <h2>
                    <Link
                        to="/trip/"
                        className={activeLink === '/trip/' ? 'active' : ''}
                        onClick={() => setActiveLink('/trip/')}
                    >
                        add trip
                    </Link>
                </h2>
            </div>
            ) : (
            <div>
                <h1>Welcome to Travel Itinerary Manager! </h1>
                <br />
                <br />
                <br />
                <h2>Start planning your trip by ...</h2>
                <br />
                <br />
                <h3>
                    <Link
                        to="/signin/"
                        className={activeLink === '/signin/' ? 'active' : ''}
                        onClick={() => setActiveLink('/signin/')}
                    >signing in</Link>
                    <div> or </div>
                    <Link
                        to="/register/"
                        className={activeLink === '/register/' ? 'active' : ''}
                        onClick={() => setActiveLink('/register/')}
                    >creating an account</Link>
                </h3>
            </div>
            )}
        </div>
    );
};

export default Home;
