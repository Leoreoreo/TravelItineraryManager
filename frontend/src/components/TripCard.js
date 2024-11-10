import { Box, Typography } from "@mui/material";
import React from "react";
import DeleteForeverIcon from "@mui/icons-material/DeleteForever";

const TripCard = ({
  trip_id,
  title,
  startDate,
  endDate,
  daysLeft,
  onDelete,
}) => {
  function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-GB", {
      weekday: "short",
      day: "numeric",
      month: "short",
      year: "numeric",
    });
  }

  return (
    <Box
      sx={{
        height: 150,
        borderRadius: 5,
        padding: 2,
        boxShadow: "1px 1px 5px rgba(0, 0, 0, 0.3)",
        display: "flex",
        alignItems: "center",
        position: "relative",
      }}
    >
      {/* Days Left Box */}
      <Box
        sx={{
          display: "inline-block",
          borderRadius: 3,
          backgroundColor: "green",
          padding: "5px 10px",
          position: "absolute",
          top: 10,
          left: 15,
        }}
      >
        <Typography variant="caption" color="white">
          {daysLeft} days to go
        </Typography>
      </Box>
      <Box
        sx={{
          borderRadius: 2,
          padding: "1px",
          position: "absolute",
          top: 10,
          right: 15,
          transition: "background-color 0.3s ease",
          "&:hover": {
            backgroundColor: "#cfd8dc",
          },
        }}
        onClick={(e) => onDelete(e, trip_id)}
      >
        <DeleteForeverIcon />
      </Box>

      {/* Location and Date Range */}
      <Box
        sx={{
          display: "flex",
          width: "100%",
          justifyContent: "space-between",
          paddingX: 1,
          alignItems: "center",
        }}
      >
        <Typography variant="h4">{title}</Typography>
        <Box>
          <Typography variant="subtitle1">{formatDate(startDate)} -</Typography>
          <Typography variant="subtitle1">{formatDate(endDate)}</Typography>
        </Box>
      </Box>
    </Box>
  );
};

export default TripCard;
