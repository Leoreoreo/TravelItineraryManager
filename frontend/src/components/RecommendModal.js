import {
  Box,
  Button,
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Grid2,
  Stack,
  TextField,
  Tooltip,
  Typography,
} from "@mui/material";
import React, { useEffect, useState } from "react";
import config from "../config";
import AddCircleOutlineIcon from "@mui/icons-material/AddCircleOutline";
import DirectionsWalkIcon from "@mui/icons-material/DirectionsWalk";
import DirectionsCarIcon from "@mui/icons-material/DirectionsCar";
import TrainIcon from "@mui/icons-material/Train";
import DirectionsBusIcon from "@mui/icons-material/DirectionsBus";
import DirectionsRailwayIcon from "@mui/icons-material/DirectionsRailway";
import AirplanemodeActiveIcon from "@mui/icons-material/AirplanemodeActive";
import DirectionsBoatIcon from "@mui/icons-material/DirectionsBoat";
import useTripStore from "../store/tripStore";
import useAuthStore from "../store/authStore";
import { useNavigate } from "react-router-dom";

export const commutes = {
  walk: <DirectionsWalkIcon />,
  car: <DirectionsCarIcon />,
  bus: <DirectionsBusIcon />,
  train: <TrainIcon />,
  railroad: <DirectionsRailwayIcon />,
  plane: <AirplanemodeActiveIcon />,
  ship: <DirectionsBoatIcon />,
};

const RecommendModal = ({
  setRecommendModalOpen,
  setRecommendTripIDs,
  loading,
  recommendTripIDs,
}) => {
  const navigate = useNavigate();

  const [recommendTrips, setRecommendTrips] = useState([]);
  const [chooseTrip, setChooseTrip] = useState(null);

  const [open, setOpen] = useState(false);
  const [title, setTitle] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [message, setMessage] = useState("");
  const uid = useAuthStore((state) => state.uid);
  const { error, addTrip } = useTripStore();

  // helper functions -----------------------------------------------------------------
  const fetchEvents = async (trip_id) => {
    try {
      const response = await fetch(
        `${config.backendUrl}/fetchevents?trip_id=${trip_id}`,
        { method: "GET" }
      );
      const data = await response.json();
      if (response.ok) {
        console.log("fetch events are ", data.events);
        return data.events;
      }
      return null;
    } catch (error) {
      console.log(error);
      return null;
    }
  };

  const addStop = async (newStop, trip_id) => {
    const response = await fetch(`${config.backendUrl}/addstop`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...newStop, trip_id }),
    });

    if (!response.ok) {
      console.log("fail to add stop");
    }

    const data = await response.json();
    console.log("[recommend modal] the add stop response is ", data);
  };

  const addCommute = async (tripEvents, commuteIndex, vehicle, trip_id) => {
    const response = await fetch(`${config.backendUrl}/addcommute`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        trip_id,
        vehicle,
        start_stop: tripEvents[commuteIndex - 1],
        end_stop: tripEvents[commuteIndex],
      }),
    });

    if (!response.ok) {
      console.log("fail to add stop");
    }

    const data = await response.json();
    console.log("[recommend modal] the add stop response is ", data);
  };

  // -------------------------------------------------------------------------------------------

  const handleClose = () => {
    setRecommendTrips([]);
    setRecommendTripIDs([]);
    setChooseTrip(null);
    setRecommendModalOpen(false);
  };

  const handleClickChoose = (tripEvents) => {
    setChooseTrip(tripEvents);
    setOpen(true);
  };

  const handleChooseClose = () => {
    setChooseTrip(null);
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

    const new_added_trip = await addTrip(uid, title, startDate, endDate);

    // already get the newly added trip
    console.log("[recommend modal] the newly added trip is ", new_added_trip);
    const new_trip_id = new_added_trip.trip_id;
    // now need to add all the events in the chosen trip into the newly added trip
    // notice the events in the chosen trip is sorted in order
    for (let i = 0; i < chooseTrip.length; i++) {
      console.log("[recommend modal] traversing the chooseTrip: ", chooseTrip[i]);
      if (chooseTrip[i].vehicle) {
        // add commute
        await addCommute(chooseTrip, i, chooseTrip[i].vehicle, new_trip_id)
      } else {
        // add stop
        await addStop(chooseTrip[i], new_trip_id);
      }
    }

    console.log("[recommend modal] the new trip's content is copied successfully");

    if (error) {
      setMessage("the error is ", error);
    } else {
      setTitle("");
      setStartDate("");
      setEndDate("");
      handleClose();
      setRecommendTrips([]);
      setRecommendTripIDs([]);
      setOpen(false);
      setChooseTrip(null);
      setRecommendModalOpen(false);
      navigate("/");
    }
  };

  useEffect(() => {
    const fetchAllEvents = async () => {
      if (!loading && recommendTripIDs.length > 0) {
        const trips = []; // Fetch the trips from the database according to the trip IDs
        for (let i = 0; i < recommendTripIDs.length; i++) {
          const trip_events = await fetchEvents(recommendTripIDs[i]);
          if (trip_events) {
            trips.push(trip_events); // Process the fetched events
          }
        }
        console.log("All trips with events:", trips);
        setRecommendTrips(trips);
      }
    };

    fetchAllEvents(); // Call the async function inside useEffect
  }, [recommendTripIDs, loading]);

  const StopCard = ({ stop, index }) => {
    return (
      <Box
        key={index}
        sx={{
          borderRadius: "50px",
          border: "1px solid green",
          padding: "1rem",
          display: "flex",
          flexDirection: "column",
        }}
      >
        <h2>{stop.title}</h2>
        <p>
          <strong>Type:</strong> {stop.type}
        </p>
        <p>
          <strong>Time Slot:</strong> {stop.startDate} - {stop.startHour}:
          {stop.startMinute} to {stop.endDate} - {stop.endHour}:{stop.endMinute}
        </p>
        <p>
          <strong>Location:</strong> {stop.location}
        </p>
        {stop.link && (
          <p>
            <strong>Link:</strong>{" "}
            <a href={stop.link} target="_blank" rel="noopener noreferrer">
              {stop.link}
            </a>
          </p>
        )}
        <p>
          <strong>Description:</strong> {stop.description}
        </p>
      </Box>
    );
  };

  return (
    <>
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
          onClick={handleClose}
        >
          close
        </button>
        {loading || recommendTrips.length === 0 ? (
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
            <Grid2 container spacing={2}>
              {recommendTrips.map((tripEvents, index) => (
                <Grid2
                  size={4}
                  key={index}
                  sx={{ display: "flex", alignItems: "center" }}
                >
                  <Box
                    sx={{
                      display: "flex",
                      flexDirection: "column",
                      height: "85%",
                    }}
                  >
                    {/* The scrollable list */}
                    <div
                      className="trip-stops-list"
                      style={{ height: "80vh", overflowY: "auto" }}
                    >
                      {tripEvents.map((event, index) =>
                        index === 0 || tripEvents[index - 1].vehicle ? (
                          <StopCard key={index} stop={event} index={index} />
                        ) : event.vehicle ? (
                          <Box
                            key={index}
                            index={index}
                            sx={{ display: "flex", alignItems: "center" }}
                          >
                            <Box>{commutes[event.vehicle.toLowerCase()]}</Box>
                          </Box>
                        ) : (
                          <Stack
                            index={index}
                            sx={{ gap: "20px", alignItems: "center" }}
                          >
                            <Tooltip title="Add Commute">
                              <AddCircleOutlineIcon />
                            </Tooltip>
                            <StopCard stop={event} index={index} />
                          </Stack>
                        )
                      )}
                    </div>

                    {/* The button with spacing */}
                    <Box
                      sx={{
                        marginTop: "16px",
                        display: "flex",
                        justifyContent: "center",
                      }}
                    >
                      <button
                        style={{ padding: "8px 16px", cursor: "pointer" }}
                        onClick={() => handleClickChoose(tripEvents)}
                      >
                        Choose
                      </button>
                    </Box>
                  </Box>
                </Grid2>
              ))}
            </Grid2>
          </Box>
        )}
      </div>

      <Dialog open={open} onClose={handleChooseClose}>
        <DialogTitle>Start this new trip!</DialogTitle>
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
            Create
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default RecommendModal;
