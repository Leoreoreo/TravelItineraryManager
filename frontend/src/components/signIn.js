import React, { useState } from 'react';
import config from '../config';
import { useNavigate } from 'react-router-dom';
import useAuthStore from '../store/authStore';

function SignIn() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const setUser = useAuthStore((state) => state.setUser); // Get setUid from the store
  const navigate = useNavigate();

  const handleSignIn = async (e) => {
    e.preventDefault();
    const response = await fetch(`${config.backendUrl}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });
    const data = await response.json();
    if (response.ok) {
      setUser(data.uid, username)
      setMessage(data.message);
      navigate('/')
    } else {
      setMessage(data.error || 'Login failed.');
    }
  };

  return (
    <div>
      <h1>Sign In</h1>
      <form onSubmit={handleSignIn}>
        <label>Username:</label>
        <input 
          type="text" 
          value={username} 
          onChange={(e) => setUsername(e.target.value)} 
          required 
        />
        <br />
        <label>Password:</label>
        <input 
          type="password" 
          value={password} 
          onChange={(e) => setPassword(e.target.value)} 
          required 
        />
        <br />
        <button type="submit">Sign In</button>
      </form>
      <div>{message}</div>
    </div>
  );
}

export default SignIn;
