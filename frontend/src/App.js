import Navbar from './components/Navbar';
import Home from './components/home'
import User from './components/user';
import Schedule from './components/schedule';
import SignIn from './components/signIn';
import Register from './components/register';
import Auth from './components/auth'
import { Routes, Route, Navigate } from 'react-router-dom';
import React, { useState, useEffect } from 'react';
import PageLayout from './layout/PageLayout';
import useAuthStore from './store/authStore';

function App() {
  const user = useAuthStore((state) => state.username)
  return (
    <PageLayout>
      <Routes>
        <Route
          path="/"
          element={user ? <Home user = {user}/> : <Navigate to="/auth/" />}
        />
        <Route
          path="/auth/"
          element={!user ? <Auth /> : <Navigate to="/"/>}
        />
        <Route path="/user/" element={<User user = {user}/>} />
        <Route path="/signin/" element={<SignIn />} />
        <Route path="/register/" element={<Register />} />
        <Route path="/trip/:trip_id" element={<Schedule />} />
      </Routes>
    </PageLayout>
  );
}

export default App;

{/* <Router>
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
</Router> */}