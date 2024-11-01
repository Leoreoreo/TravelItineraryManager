import Navbar from './components/Navbar';
import Home from './components/home'
import User from './components/user';
import Schedule from './components/schedule';
import SignIn from './components/signIn';
import Register from './components/register';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import React, { useState, useEffect } from 'react';

function App() {
  const [user, setUser] = useState(null);
  return (
    <Router>
      <div className="App">
        <Navbar user = {user}/>
        <Switch>
          <Route exact path="/">
            <Home user = {user}/>
          </Route>
          <Route exact path="/user/">
            <User user = {user}/>
          </Route>
          <Route exact path="/signin/">
            <SignIn setUser = {setUser}/>
          </Route>
          <Route exact path="/register/">
            <Register />
          </Route>
          <Route exact path="/trip/">
            <Schedule />
          </Route>
        </Switch>
      </div>
    </Router>
  );
}

export default App;
