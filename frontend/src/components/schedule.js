// Schedule.js
import React, { useState, useEffect } from "react";
import GoogleMap from "./googleMap";
import AddStop from "./addStop"; // Import the AddStop component
import { useParams } from "react-router-dom";
import config from "../config";
import { accordionClasses } from "@mui/material";

const Schedule = () => {
  const { trip_id } = useParams();

  const [fadeIn, setFadeIn] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [tripStops, setTripStops] = useState([]); // State to hold the trip stops

  useEffect(() => {
    setFadeIn(true);
  }, []);

  useEffect(() => {
    const fetchStops = async () => {
      try {
        const response = await fetch(
          `${config.backendUrl}/fetchstops?trip_id=${trip_id}`,
          { method: "GET" }
        );
        const data = await response.json();
        if (response.ok) {
          setTripStops(data.stops);
        }
      } catch (error) {
        console.log(error);
      }
    };

    fetchStops();
  }, [trip_id]);

  const handleAddClick = () => {
    setShowModal(true); // Open the modal when "Add" is clicked
  };

  const handleSaveTripStop = (newStop) => {
    fetch(`${config.backendUrl}/addstop`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...newStop, trip_id }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("event_id is ", data.event_id);
        setTripStops([...tripStops, newStop]); // Append the new trip stop
        setShowModal(false); // Close the modal after saving
      })
      .catch((error) => [console.log(error)]);
  };

  return (
    <div>
      <GoogleMap />
      <div className="schedule">
        <h1>New Trip</h1>
        <button onClick={handleAddClick}>Add Trip Stop</button>

        {/* Render the list of trip stops */}
        <ul>
          {tripStops.map((stop, index) => (
            <li key={index}>
              <strong>{stop.title}</strong> - {stop.description} from{" "}
              {stop.startDate} to {stop.endDate}
            </li>
          ))}
        </ul>
      </div>

      {showModal && (
        <div className="modal">
          <AddStop
            onSave={handleSaveTripStop}
            onCancel={() => setShowModal(false)}
          />
        </div>
      )}
    </div>
  );
};

export default Schedule;
