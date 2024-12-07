import {
  Box,
  FormControl,
  MenuItem,
  Select,
  TextField,
  Typography,
} from "@mui/material";
import React, { useState } from "react";
import useAuthStore from "../store/authStore";
import config from "../config";
import { motion } from "framer-motion";

const alltraits = [
  "Sightseer",
  "Adventurer",
  "Historian",
  "Artist",
  "Foodie",
  "Family",
  "Solo",
  "Nature",
  "Luxury",
  "Budget",
];

const OnBoardModal = ({ close }) => {
  const setTrait = useAuthStore((state) => state.setTrait);
  const setBOD = useAuthStore((state) => state.setBOD);
  const uid = useAuthStore((state) => state.uid);

  const [newBod, setNewBod] = useState("");
  const [newTrait, setNewTrait] = useState("");

  const handleConfirm = async () => {
    let response = await fetch(`${config.backendUrl}/updatebod`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ uid, newBod }),
    });

    let data = await response.json();
    console.log("the response data is ", data);
    setBOD(newBod);

    response = await fetch(`${config.backendUrl}/updatetrait`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ uid, newTrait }),
    });

    data = await response.json();
    console.log("the response data is ", data);
    setTrait(newTrait);

    close();
  };

  return (
    <motion.div
      key="onBoardModal"
      className="modal"
      style={{ background: "black", color: "white", opacity: 1 }}
      initial={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{
        duration: 0.5,
        type: "spring", // have the spring effect
        ease: "easeInOut",
      }}
    >
      <Box sx={{ display: "flex", flexDirection: "column", color: "white", position: "relative", height: "70%" }}>
        <motion.div
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{
            duration: 0.5,
            type: "spring", // have the spring effect
            ease: "easeInOut",
          }}
        >
          <Typography variant="h3" sx={{ color: "white" }}>
            Welcome To
          </Typography>
          <Typography
            sx={{
              fontFamily: "'Sour Gummy', sans-serif",
              fontStyle: "normal",
              fontSize: "10rem",
              textShadow: "2px 2px 4px rgba(0, 0, 0, 0.3)",
              letterSpacing: "2px",
              color: "white",
            }}
          >
            TIM
          </Typography>
        </motion.div>
        <motion.div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: "10px",
            margin: "10px",
          }}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{
            duration: 0.5,
            delay: 1,
            type: "spring", // have the spring effect
            ease: "easeInOut",
          }}
        >
          <Typography sx={{ color: "white" }}>
            What is your birthday?
          </Typography>
          <TextField
            hiddenLabel
            size="small"
            type="date"
            value={newBod}
            onChange={(e) => setNewBod(e.target.value)}
            sx={{
              input: {
                color: "white", // Text color
              },
              "& .MuiOutlinedInput-root": {
                "& fieldset": {
                  borderColor: "white", // Border color
                },
                "&:hover fieldset": {
                  borderColor: "white", // Border color on hover
                },
              },
              '& input[type="date"]::-webkit-calendar-picker-indicator': {
                filter: "invert(1)", // Inverts the color of the calendar icon to make it visible
              },
            }}
          />
        </motion.div>
        <motion.div
          style={{ display: "flex", flexDirection: "column", gap: "10px" }}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{
            duration: 0.5,
            delay: 2,
            type: "spring", // have the spring effect
            ease: "easeInOut",
          }}
        >
          <Typography sx={{ color: "white" }}>
            What type of traveller are you?
          </Typography>
          <FormControl
            sx={{
              m: 1,
              minWidth: 120,
              "& .MuiOutlinedInput-notchedOutline": {
                borderColor: "white", // Default border color
              },
              "& .MuiOutlinedInput-root": {
                "&:hover .MuiOutlinedInput-notchedOutline": {
                  borderColor: "gray", // Border color on hover
                },
              },
              "& .MuiSelect-root": {
                color: "white", // Ensures the selected text is white
              },
              "& .MuiSvgIcon-root": {
                color: "white", // Dropdown arrow icon color
              },
            }}
          >
            <Select
              defaultValue={newTrait}
              onChange={(event) => setNewTrait(event.target.value)}
              displayEmpty
              sx={{
                color: "white", // Ensures the selected text remains white
                "& .MuiSelect-icon": {
                  color: "white", // Dropdown arrow icon color
                },
              }}
              MenuProps={{
                PaperProps: {
                  sx: {
                    backgroundColor: "black", // Dropdown menu background color
                    color: "white", // Menu item text color
                  },
                },
              }}
            >
              {alltraits.map((trait, index) => (
                <MenuItem
                  key={index}
                  value={trait}
                  sx={{
                    color: "white", // Menu item text color
                    backgroundColor: "black", // Menu item background color
                    "&.Mui-selected": {
                      backgroundColor: "gray", // Background for selected item
                      color: "white", // Text color for selected item
                    },
                    "&.Mui-selected:hover": {
                      backgroundColor: "darkgray", // Background when selected and hovered
                      color: "white", // Text color when selected and hovered
                    },
                    "&:hover": {
                      backgroundColor: "gray", // Background color on hover
                    },
                  }}
                >
                  {trait}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </motion.div>
        {newBod && newTrait && (
          <button
            style={{ background: "white", color: "black", alignSelf: "end", position:"absolute", bottom: 70 }}
            onClick={handleConfirm}
            
          >
            confirm
          </button>
        )}
      </Box>
    </motion.div>
  );
};

export default OnBoardModal;
