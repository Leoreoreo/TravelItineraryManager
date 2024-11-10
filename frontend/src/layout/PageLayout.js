import React from "react";
import Navbar from "../components/Navbar";
import { useLocation } from "react-router-dom";
import Grid from "@mui/material/Grid2";
import { Box, Container, Typography } from "@mui/material";

const PageLayout = ({ children }) => {
  const { pathname } = useLocation();

  const showLeftWelcome = pathname === "/signin/" || pathname === "/register/";

  return (
    <div className="App">
      <Navbar />
      {showLeftWelcome ? (
        <Grid container>
          <Grid size={6}>
            <Container>
              <Box
                sx={{
                  display: "flex",
                  flexDirection: "column",
                  justifyContent: "center",
                  alignItems: "center",
                  height: "90vh",
                }}
              >
                <Typography variant="h3">Welcome To</Typography>
                <Typography
                  sx={{
                    fontFamily: "'Sour Gummy', sans-serif",
                    fontStyle: "normal",
                    fontSize: "10rem",
                    textShadow: "2px 2px 4px rgba(0, 0, 0, 0.3)",
                    letterSpacing: "2px",
                  }}
                >
                  TIM
                </Typography>
                <Typography variant="subtitle2">
                  Travel Itinerary Manager
                </Typography>
              </Box>
            </Container>
          </Grid>
          <Grid size={6}>
            <Container>
              <Box
                sx={{
                  display: "flex",
                  flexDirection: "column",
                  justifyContent: "center",
                  alignItems: "center",
                  height: "90vh",
                }}
              >
                {children}
              </Box>
            </Container>
          </Grid>
        </Grid>
      ) : (
        <div>{children}</div>
      )}
    </div>
  );
};

export default PageLayout;
