import { Link } from 'react-router-dom';
import React, { useState, useEffect } from 'react';

function SignIn({ setUser }) {
  const [username, setUsername] = useState('');
  const [activeLink, setActiveLink] = useState('/');

  const handleSignIn = (e) => {
    // TODO: check if the username-password pair is valid
    setUser(username); // Set the user to the entered username
    setActiveLink('/');
  };

  return (
    <div>
      <br />
      <h1>SIGN IN</h1>
      <br />
      <form onSubmit={handleSignIn}>
        <label>Username:</label>
        <input 
          type="text" 
          id="username" 
          name="username" 
          required 
          value={username} 
          onChange={(e) => setUsername(e.target.value)} 
        />
        <br />
        <label>Password:</label>
        <input type="password" id="password" name="password" required />
        <br />
        <div className='links'>
            <Link 
                to="/" 
                className={activeLink === '/' ? 'active' : ''} 
                onClick={handleSignIn}
                >Sign In
            </Link>
        </div>
      </form>
    </div>
  );
}

export default SignIn;
