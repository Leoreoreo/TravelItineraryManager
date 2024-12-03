import { useEffect, useState } from "react";
import useAuthStore from "../store/authStore";
import {
  Box,
  FormControl,
  MenuItem,
  Select,
  TextField,
  Typography,
} from "@mui/material";
import config from "../config";

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

const User = ({ user }) => {
  const bod = useAuthStore((state) => state.bod);
  const trait = useAuthStore((state) => state.trait);
  const uid = useAuthStore((state) => state.uid);

  const setTrait = useAuthStore((state) => state.setTrait);
  const setBOD = useAuthStore((state) => state.setBOD);

  const [newBod, setNewBod] = useState(bod);
  const [newTrait, setNewTrait] = useState(trait);

  useEffect(() => {
    if (newBod) {
      fetch(`${config.backendUrl}/updatebod`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ uid, newBod }),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log("the response data is ", data);
          setBOD(newBod);
        })
        .catch((error) => console.log(error));
    }
  }, [newBod]);

  useEffect(() => {
    if (newTrait) {
      fetch(`${config.backendUrl}/updatetrait`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ uid, newTrait }),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log("the response data is ", data);
          setTrait(newTrait);
        })
        .catch((error) => console.log(error));
    }
  }, [newTrait]);

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        gap: 1,
      }}
    >
      <h1>User: {user} </h1>
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          gap: 3,
        }}
      >
        <Typography>What is your birthday?</Typography>
        <TextField
          hiddenLabel
          size="small"
          type="date"
          value={newBod}
          onChange={(e) => setNewBod(e.target.value)}
        />
      </Box>

      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
        }}
      >
        <Typography>What type of traveller are you?</Typography>
        <FormControl sx={{ m: 1, minWidth: 120 }}>
          <Select
            defaultValue={newTrait}
            onChange={(event) => setNewTrait(event.target.value)}
            displayEmpty
          >
            {alltraits.map((trait, index) => (
              <MenuItem key={index} value={trait}>
                {trait}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>
    </Box>
  );
};

export default User;
