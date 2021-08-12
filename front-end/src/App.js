import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

import Home from "./components/Home/Home.js";
import ShoppingCart from "./components/ShoppingCart/ShoppingCart.js";
import Login from "./components/Login.js";

function App() {
  return (
    <div>
      <Router>
        <Switch>
          <Route path="/shopping-cart">
            <ShoppingCart />
          </Route>

          <Route path="/login">
            <Login />
          </Route>

          <Route path="/about">
            <About />
          </Route>

          <Route path="/">
            <Home />
          </Route>
        </Switch>
      </Router>
    </div>
  );
}

export default App;

// JUST FOR DEV

function About() {
  return <h2>About</h2>;
}
