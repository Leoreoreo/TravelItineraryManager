import {
  Box,
  Button,
  Card,
  CardContent,
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControl,
  IconButton,
  Input,
  InputAdornment,
  InputLabel,
  OutlinedInput,
  TextField,
  Typography,
} from "@mui/material";
import { useState, useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import useAuthStore from "../store/authStore";
import useTripStore from "../store/tripStore";
import TripCard from "./TripCard";
import OnBoardModal from "./onBoardModal";
import AutoAwesomeIcon from "@mui/icons-material/AutoAwesome";
import ArrowUpwardIcon from "@mui/icons-material/ArrowUpward";
import { AnimatePresence, motion } from "framer-motion";
import config from "../config";

const Home = ({ user }) => {
  const [activeLink, setActiveLink] = useState("/");
  const [open, setOpen] = useState(false);
  const [title, setTitle] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [message, setMessage] = useState("");
  const uid = useAuthStore((state) => state.uid);
  const { trips, error, fetchTrips, addTrip, removeTrip } = useTripStore();

  // for first time user on board
  const trait = useAuthStore((state) => state.trait);
  const bod = useAuthStore((state) => state.bod);
  const firstTimeUser = !Boolean(trait && bod);
  const [showOnBoardModal, setShowOnBoardModal] = useState(firstTimeUser);

  // for the gpt helper
  const boxRef = useRef(null);
  const [showInput, setShowInput] = useState(false);
  const [userInput, setUserInput] = useState("");
  const [generating, setGenerating] = useState(false);
  const handleButtonClick = () => {
    setShowInput(true);
  };
  // if click outside the box, the input field will disappear
  const handleClickOutside = (event) => {
    // Check if the click is outside the referenced box
    if (boxRef.current && !boxRef.current.contains(event.target)) {
      setShowInput(false);
    }
  };
  useEffect(() => {
    // Add event listener for clicks on the document
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      // Cleanup the event listener on component unmount
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const handleGenerate = async () => {
    if (userInput.length === 0) return;

    try {
      setGenerating(true);
      const response = await fetch(`${config.backendUrl}/generate_gpt_trip`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ uid, user_input: userInput }),
      });

      if (!response.ok) {
        console.log("cannot generate");
      }

      const data = await response.json();
      console.log(
        "[home] successfully generate the trip, the response is ",
        data
      );
    } catch (error) {
      console.log("[home] generate trip: ", error);
    } finally {
      setGenerating(false);
      setUserInput("");
      fetchTrips(uid);
    }
  };

  useEffect(() => {
    setActiveLink("/");
  }, []);

  function getDaysFromTodayToStartDate(startDate) {
    const start = new Date(startDate);

    // Get today's date with time set to midnight
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    // Calculate the difference in milliseconds
    const diffInMs = start - today;

    // Convert milliseconds to days
    const diffInDays = Math.round(diffInMs / (1000 * 60 * 60 * 24));

    return diffInDays;
  }

  useEffect(() => {
    if (uid && trips.length === 0) {
      fetchTrips(uid);
    }
  }, [uid]);

  const handleOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleAddTrip = async () => {
    if (title.trim().length === 0) {
      setMessage("please enter the title");
      return;
    }
    if (startDate === "" || endDate === "") {
      setMessage("please enter the date");
      return;
    }
    if (!uid) {
      setMessage("please login first");
      return;
    }

    setMessage("");

    await addTrip(uid, title, startDate, endDate); // later need to add start date and end date
    if (error) {
      setMessage("the error is ", error);
    } else {
      setTitle("");
      setStartDate("");
      setEndDate("");
      handleClose();
    }
  };

  const handleDelete = (event, trip_id) => {
    event.preventDefault();
    removeTrip(trip_id);
  };

  // the trip card component

  return (
    <div>
      <Box
        sx={{ width: 400, display: "flex", gap: 3, flexDirection: "column" }}
      >
        <Box
          sx={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <Typography variant="h4">Trips</Typography>
          <Typography
            sx={{
              color: "#2196f3",
              cursor: "pointer",
              "&:hover": { color: "#1976d2" },
            }}
            onClick={handleOpen}
          >
            + Create a trip
          </Typography>
        </Box>
        {trips &&
          trips.map(({ trip_id, trip_name, start_date, end_date }) => (
            <Link
              key={trip_id}
              to={`/trip/${trip_id}`}
              onClick={() => setActiveLink(`/trip/${trip_id}`)}
              style={{ textDecoration: "none" }}
            >
              <TripCard
                trip_id={trip_id}
                title={trip_name}
                startDate={start_date}
                endDate={end_date}
                daysLeft={getDaysFromTodayToStartDate(start_date)}
                onDelete={handleDelete}
              />
            </Link>
          ))}
      </Box>
      <Box
        ref={boxRef}
        sx={{
          position: "fixed",
          bottom: 20,
          left: 0,
          width: "100vw",
          height: "60px",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            gap: 2,
            position: "relative", // Ensure smooth positioning
          }}
        >
          <motion.div
            onClick={handleButtonClick}
            layout
            style={{
              cursor: "pointer",
              boxShadow: "0px 4px 8px rgba(0, 0, 0, 0.2)",
              borderRadius: "50%",
              padding: "10px",
              backgroundColor: "#fff",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            <AutoAwesomeIcon />
          </motion.div>

          {showInput && (
            <motion.div
              key="input"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.5, ease: "easeInOut" }}
              layout
            >
              <FormControl sx={{ m: 1, width: "400px" }} variant="standard">
                <Input
                  id="standard-adornment-password"
                  placeholder="What can I help you create?"
                  value={userInput}
                  onChange={(event) => setUserInput(event.target.value)}
                  endAdornment={
                    <InputAdornment position="end">
                      {!generating ? (
                        <div className="submit" onClick={handleGenerate}>
                          <ArrowUpwardIcon />
                        </div>
                      ) : (
                        <div
                          style={{ marginBottom: "10px", padding: "5px" }}
                          onClick={handleGenerate}
                        >
                          <CircularProgress size="30px" />
                        </div>
                      )}
                    </InputAdornment>
                  }
                />
              </FormControl>
              {/* <TextField
                variant="standard"
                placeholder="What can I help you create?"
                autoFocus
                sx={{ width: "400px" }}
                value={userInput}
                onChange={(event) => setUserInput(event.target.value)}
              /> */}
            </motion.div>
          )}
        </Box>
      </Box>
      {/* <button
                className="delete-trip-button"
                onClick={() => handleDelete(trip_id)}
              >
                x
              </button> */}

      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Start a new trip!</DialogTitle>
        <DialogContent>
          <Box
            sx={{
              display: "flex",
              gap: 2,

              flexDirection: "column",
            }}
          >
            <Typography variant="subtitle1" sx={{ textAlign: "start" }}>
              Title:
            </Typography>
            <TextField
              hiddenLabel
              fullWidth
              type="text"
              size="small"
              value={title}
              onChange={(event) => setTitle(event.target.value)}
            />

            <Typography variant="subtitle1" sx={{ textAlign: "start" }}>
              Start Date:
            </Typography>
            <TextField
              hiddenLabel
              fullWidth
              type="date"
              size="small"
              value={startDate}
              onChange={(event) => setStartDate(event.target.value)}
            />
            <Typography variant="subtitle1" sx={{ textAlign: "start" }}>
              End Date:
            </Typography>
            <TextField
              hiddenLabel
              fullWidth
              type="date"
              size="small"
              value={endDate}
              onChange={(event) => setEndDate(event.target.value)}
            />
          </Box>
          {message.length !== 0 && (
            <Typography variant="h6" color="red">
              {message}
            </Typography>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleAddTrip} color="black" autoFocus>
            Add
          </Button>
        </DialogActions>
      </Dialog>

      <AnimatePresence mode="wait">
        {showOnBoardModal && (
          <OnBoardModal
            key="onBoardModal"
            close={() => setShowOnBoardModal(false)}
          />
        )}
      </AnimatePresence>
    </div>
  );
};

export default Home;
