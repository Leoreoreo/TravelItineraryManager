import { Box, CircularProgress, Grid2, Typography } from "@mui/material";
import React from "react";

const fakeTrips = [1, 2, 3];

const RecommendModal = ({ onClose, loading, recommendTrips }) => {
  return (
    <div
      class="event-modal"
      style={{
        width: "80%",
        height: "80%",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <button
        style={{ position: "absolute", right: 5, top: 5 }}
        onClick={onClose}
      >
        close
      </button>
      {loading ? (
        <Box
          sx={{
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
            gap: 1,
          }}
        >
          <CircularProgress />
          <Typography>loading the top recommended trips ...</Typography>
        </Box>
      ) : (
        <Box sx={{ width: "100%" }}>
          <Grid2 container>
            {fakeTrips.map((trip, index) => (
              <Grid2 size={4} key={index}>
                {trip}
              </Grid2>
            ))}
          </Grid2>
        </Box>
      )}
    </div>
  );
};

export default RecommendModal;
