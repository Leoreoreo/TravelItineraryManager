import { Link } from "react-router-dom";
import { useState } from "react";

const Auth = () => {
  const [activeLink, setActiveLink] = useState("/");

  return (
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
          className={activeLink === "/signin/" ? "active" : ""}
          onClick={() => setActiveLink("/signin/")}
        >
          signing in
        </Link>
        <div> or </div>
        <Link
          to="/register/"
          className={activeLink === "/register/" ? "active" : ""}
          onClick={() => setActiveLink("/register/")}
        >
          creating an account
        </Link>
      </h3>
    </div>
  );
};

export default Auth;
