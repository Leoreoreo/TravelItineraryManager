// Schedule.js
import React, { useState, useEffect } from "react";
import MapComponent from "./googleMap";
import AddStop from "./addStop"; // Import the AddStop component
import { useParams } from "react-router-dom";
import config from "../config";

import {
  accordionClasses,
  Box,
  FormControl,
  Menu,
  MenuItem,
  Select,
  Stack,
  Tooltip,
  Typography,
} from "@mui/material";
import useTripStore from "../store/tripStore";
import DirectionsWalkIcon from "@mui/icons-material/DirectionsWalk";
import DirectionsCarIcon from "@mui/icons-material/DirectionsCar";

import AddCircleOutlineIcon from "@mui/icons-material/AddCircleOutline";
import TrainIcon from "@mui/icons-material/Train";
import DirectionsBusIcon from "@mui/icons-material/DirectionsBus";
import DirectionsRailwayIcon from "@mui/icons-material/DirectionsRailway";
import AirplanemodeActiveIcon from "@mui/icons-material/AirplanemodeActive";
import DirectionsBoatIcon from "@mui/icons-material/DirectionsBoat";
import useAuthStore from "../store/authStore";
import RecommendModal from "./RecommendModal";

const commutes = {
  walk: <DirectionsWalkIcon />,
  car: <DirectionsCarIcon />,
  bus: <DirectionsBusIcon />,
  train: <TrainIcon />,
  railroad: <DirectionsRailwayIcon />,
  plane: <AirplanemodeActiveIcon />,
  ship: <DirectionsBoatIcon />,
};

const Schedule = () => {
  const { trip_id } = useParams();

  // user id
  const uid = useAuthStore((state) => state.uid);

  const trips = useTripStore((state) => state.trips); // used to get the info of this specific trip
  const trip = trips.find((trip) => trip.trip_id.toString() === trip_id); // get the info of this specific trip
  const [fadeIn, setFadeIn] = useState(false);
  const [showStopModal, setShowStopModal] = useState(false);
  const [anchorEl, setAnchorEl] = useState(null);
  const [commuteIndex, setCommuteIndex] = useState(null); // the index of the empty commute button that we click
  const [vehicle, setVehicle] = useState("walk");
  const [tripEvents, setTripEvents] = useState([]); // State to hold the trip stops
  const [editingStop, setEditingStop] = useState(null); // State to track the stop being edited
  const [addresses, setAddresses] = useState([]);

  // recommend
  const [recommendModalOpen, setRecommendModalOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [recommendTripIDs, setRecommendTripIDs] = useState([]);

  const sortEvents = (events) => {
    events.sort((a, b) => {
      // Compare startDate first
      if (a.startDate !== b.startDate) {
        return new Date(a.startDate) - new Date(b.startDate);
      }

      // If startDate is the same, compare startHour
      if (a.startHour !== b.startHour) {
        return a.startHour - b.startHour;
      }

      if (a.startMinute !== b.startMinute) {
        return a.startHour - b.startHour;
      }

      if (a.endDate !== b.endDate) {
        return new Date(a.endDate) - new Date(b.endDate);
      }

      if (a.endMinute !== b.endMinute) {
        return a.endHour - b.endHour;
      }

      if (a.endMinute !== b.endMinute) {
        return a.endHour - b.endHour;
      }
    });

    return events;
  };

  // sort the events every time new events are added
  useEffect(() => {
    console.log("trip events are ", tripEvents);
  }, [tripEvents]);

  useEffect(() => {
    setFadeIn(true);
  }, []);

  // Fetch stops when component mounts
  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const response = await fetch(
          `${config.backendUrl}/fetchevents?trip_id=${trip_id}`,
          { method: "GET" }
        );
        const data = await response.json();
        if (response.ok) {
          console.log("fetch events are ", data.events);
          setTripEvents(data.events);
        }
      } catch (error) {
        console.log(error);
      }
    };

    fetchEvents();
  }, [trip_id]);

  // Automatically update addresses when tripStops changes
  // useEffect(() => {
  //   const locations = tripStops.map((stop) => stop.location).filter(Boolean);
  //   setAddresses(locations);
  //   console.log("Updated addresses:", locations);
  // }, [tripStops]);

  //const handleAddClick = () => {

  const handleAddStopClick = () => {
    setEditingStop(null); // Reset editingStop when adding a new stop
    setShowStopModal(true);
  };

  const handleRecommendClick = async () => {
    if (loading) return;

    setLoading(true);
    setRecommendModalOpen(true);

    const response = await fetch(`${config.backendUrl}/recommend_trips`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ uid, tid: trip_id }),
    });

    if (!response.ok) {
      console.log("the recommend api fails");
      setLoading(false);
      setRecommendModalOpen(false);
    }

    const data = await response.json();
    setRecommendTripIDs(data.tid_recs);
    console.log("[schedule] the recommend trip ids are ", data.tid_recs);

    setLoading(false);
  };

  const handleAddCommuteClick = (event, index) => {
    console.log("click commute button, index is ", index);
    console.log("corresponding event is ", tripEvents[index]);
    setCommuteIndex(index);
    setAnchorEl(event.currentTarget);
  };

  const handleAddTripStop = (newStop) => {
    fetch(`${config.backendUrl}/addstop`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...newStop, trip_id }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("event_id is ", data.event_id);
        newStop.event_id = data.event_id;

        let newTripEvents = [...tripEvents, newStop];
        newTripEvents = sortEvents(newTripEvents);
        setTripEvents(newTripEvents);
        setShowStopModal(false); // Close the modal after saving
      })
      .catch((error) => console.log(error));
  };

  // add the commute into database
  const handleAddTripCommute = () => {
    console.log("handle add trip commute, vehicle is ", vehicle);
    console.log("events are ", tripEvents);
    fetch(`${config.backendUrl}/addcommute`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        trip_id,
        vehicle,
        start_stop: tripEvents[commuteIndex - 1],
        end_stop: tripEvents[commuteIndex],
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("commute is ", data.commute);
        let newTripEvents = [...tripEvents, data.commute];
        newTripEvents = sortEvents(newTripEvents);
        setTripEvents(newTripEvents);
        setAnchorEl(null); // close the menu for add commute
        setVehicle("walk");
      })
      .catch((error) => console.log(error));
  };

  const handleEditClick = (index) => {
    setEditingStop(index);
    setShowStopModal(true);
  };

  const handleEditTripStop = (tripStop) => {
    console.log("trip stop is", tripStop);
    fetch(`${config.backendUrl}/editstop`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...tripStop }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("event_id is ", data.event_id);
        // <<<<<<< HEAD
        //         const updatedStops = tripStops.map((stop) =>
        //           stop.event_id === tripStop.event_id ? tripStop : stop
        //         );
        //         setTripStops(updatedStops); // Update tripStops
        //         setShowModal(false); // Close the modal after saving
        // =======
        const trip = data.trip;
        let newTrip = [];
        for (const t of tripEvents) {
          if (t.event_id == trip.event_id) {
            newTrip.push(trip);
          } else {
            newTrip.push(t);
          }
        }

        // delete the commute method related to the edited stop event
        for (let i = 0; i < newTrip.length; i++) {
          if (newTrip[i].event_id === trip.event_id) {
            let prev = null;
            let next = null;
            if (i > 0 && newTrip[i - 1].vehicle) {
              prev = newTrip[i - 1];
            }

            if (i < newTrip.length - 1 && newTrip[i + 1].vehicle) {
              next = newTrip[i + 1];
            }

            if (prev) {
              handleDeleteClick(prev);
            }
            if (next) {
              handleDeleteClick(next);
            }
            break;
          }
        }

        newTrip = sortEvents(newTrip);
        setTripEvents(newTrip);
        setShowStopModal(false); // Close the modal after saving
      })
      .catch((error) => console.log(error));
  };

  const handleDeleteClick = (delete_event) => {
    //console.log("event is ", tripEvents[index]);
    fetch(`${config.backendUrl}/deleteevent`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ event: delete_event }),
    })
      .then((response) => response.json())
      .then(() => {
        setTripEvents((events) =>
          events.filter((event) => event.event_id !== delete_event.event_id)
        );
      })
      .catch((error) => console.log(error));
  };

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
        <Box sx={{ display: "flex", justifyContent: "flex-end", gap: "5px" }}>
          <button onClick={() => handleEditClick(index)}>Edit</button>
          <button onClick={() => handleDeleteClick(tripEvents[index])}>
            Delete
          </button>
        </Box>
      </Box>
    );
  };

  // const addresses = [
  //   "Knott Hall, Notre Dame, IN",
  //   "Debartoo Hall, Notre Dame, IN",
  //   "Potawatomi Zoo, South Bend, IN",
  // ];
  return (
    <div>
      <Box className="googleMap">
        <MapComponent addresses={addresses} />
      </Box>

      <div className="schedule">
        <h1>{trip.trip_name}</h1>
        <button onClick={handleAddStopClick} style={{ marginBottom: "20px" }}>
          Add Trip Stop
        </button>
        {tripEvents.length > 0 && (
          <button
            onClick={handleRecommendClick}
            style={{ marginBottom: "20px" }}
          >
            Recommend Similar Trips
          </button>
        )}

        {/* Render the list of trip stops */}
        <div className="trip-stops-list">
          {tripEvents.map((event, index) =>
            index === 0 || tripEvents[index - 1].vehicle ? ( // the first event is always stop, or if the last event is vehicle
              <StopCard key={index} stop={event} index={index} />
            ) : event.vehicle ? ( // if this is already a commute, then display the commute icon
              <Box
                index={index}
                sx={{ display: "flex", alignItems: "center", gap: 2 }}
              >
                <Box>{commutes[event.vehicle.toLowerCase()]}</Box>

                <button onClick={() => handleDeleteClick(tripEvents[index])}>
                  x
                </button>
              </Box>
            ) : (
              // otherwise, we need to have a button that allows user to add commute between two stops
              <Stack index={index} sx={{ gap: "50px", alignItems: "center" }}>
                <Tooltip title="Add Commute">
                  <button
                    style={{
                      backgroundColor: "transparent",
                      border: "none",
                      boxShadow: "none",
                    }}
                    onClick={(event) => handleAddCommuteClick(event, index)}
                  >
                    <AddCircleOutlineIcon />
                  </button>
                </Tooltip>
                <StopCard stop={event} index={index} />
              </Stack>
            )
          )}
        </div>
      </div>

      {showStopModal && (
        <div className="modal">
          <AddStop
            onAdd={handleAddTripStop}
            onEdit={handleEditTripStop}
            onCancel={() => setShowStopModal(false)}
            initialData={editingStop !== null ? tripEvents[editingStop] : null} // Pass the stop to edit or null
          />
        </div>
      )}
      {recommendModalOpen && (
        <div class="modal">
          <RecommendModal
            setRecommendModalOpen = {setRecommendModalOpen}
            setRecommendTripIDs = {setRecommendTripIDs}
            loading={loading}
            recommendTripIDs={recommendTripIDs}
          />
        </div>
      )}
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={() => setAnchorEl(null)}
      >
        <Box
          sx={{
            margin: "10px",
            display: "flex",
            flexDirection: "column",
            alignItems: "start",
          }}
        >
          <Typography>Select Commute Type</Typography>
          <FormControl sx={{ m: 1, minWidth: 120 }}>
            <Select
              defaultValue={"walk"}
              onChange={(event) => setVehicle(event.target.value)}
              displayEmpty
            >
              <MenuItem value={"walk"}>Walk</MenuItem>
              <MenuItem value={"car"}>Car</MenuItem>
              <MenuItem value={"bus"}>Bus</MenuItem>
              <MenuItem value={"train"}>Train</MenuItem>
              <MenuItem value={"railroad"}>railroad</MenuItem>
              <MenuItem value={"plane"}>Plane</MenuItem>
              <MenuItem value={"ship"}>Ship</MenuItem>
            </Select>
          </FormControl>
          <button style={{ alignSelf: "end" }} onClick={handleAddTripCommute}>
            add
          </button>
        </Box>
      </Menu>
    </div>
  );
};

export default Schedule;
