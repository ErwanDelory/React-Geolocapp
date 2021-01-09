import React from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import './css/app.css';
import NavbarApp from './components/navbar';
import Footer from './components/footer';
import Home from './pages/home';

const App = () => {
  return (
    <div>
      <Router>
        <NavbarApp title={'GeolocApp'} />
        <Switch>
          <Route exact path="/" component={Home} />
        </Switch>
        <br />
        <Footer title={'Copyright © 2021 - GeolocApp'} />
      </Router>
    </div>
  );
};
export default App;
