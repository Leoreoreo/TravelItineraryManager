import Navbar from './components/Navbar';
import Home from './components/home'
import User from './components/user';
import GoogleMap from './components/googleMap';
import Schedule from './components/schedule';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <Switch>
          <Route exact path="/">
            <Home />
          </Route>
          <Route exact path="/user/">
            <User />
          </Route>
        </Switch>
        <Switch>
          <Route exact path="/travel/">
            <GoogleMap />
            <Schedule />
          </Route>
        </Switch>
      </div>
    </Router>
  );
}

export default App;
