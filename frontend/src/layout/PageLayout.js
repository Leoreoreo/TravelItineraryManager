import React from "react";
import Navbar from "../components/Navbar";

const PageLayout = ({ children }) => {
  return (
    <div className="App">
      <Navbar />
      <div>{children}</div>
    </div>
  );
};

export default PageLayout;
