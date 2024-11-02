import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import { BrowserRouter } from "react-router-dom";
import { ThemeProvider, createMuiTheme } from "@mui/material/styles";

const root = ReactDOM.createRoot(document.getElementById("root"));

const theme = createMuiTheme();

root.render(
  // start rendering
  // JSX language
  // App: a function (App.js)
  <BrowserRouter>
    <ThemeProvider theme={theme}>
      <React.StrictMode>
        <App />
      </React.StrictMode>
    </ThemeProvider>
  </BrowserRouter>
);
