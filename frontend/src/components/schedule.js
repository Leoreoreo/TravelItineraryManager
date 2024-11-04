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
  const [editingStop, setEditingStop] = useState(null); // State to track the stop being edited

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
    setEditingStop(null); // Reset editingStop when adding a new stop
    setShowModal(true);
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
        <div className="trip-stops-list">
          {tripStops.map((stop, index) => (
            <li key={index}>
              <strong>{stop.title}</strong> - {stop.description} from{" "}
              {stop.startDate} to {stop.endDate}
            </li>
//             <div
//               key={index}
//               className="trip-stop-card"
//               onClick={() => handleEditTripStop(index)}
//             >
//               <h2>{stop.title}</h2>
//               <p><strong>Type:</strong> {stop.type}</p>
//               <p>
//                 <strong>Time Slot:</strong> {stop.date} - {stop.startHour}:{stop.startMinute} to {stop.endHour}:{stop.endMinute}
//               </p>
//               <p><strong>Location:</strong> {stop.location}</p>
//               {stop.link && (
//                 <p>
//                   <strong>Link:</strong> <a href={stop.link} target="_blank" rel="noopener noreferrer">{stop.link}</a>
//                 </p>
//               )}
//               <p><strong>Description:</strong> {stop.description}</p>
//             </div>
          ))}
        </div>
      </div>

      {showModal && (
        <div className="modal">
          <AddStop
            onSave={handleSaveTripStop}
            onCancel={() => setShowModal(false)}

//             initialData={editingStop !== null ? tripStops[editingStop] : null} // Pass the stop to edit or null
          />
        </div>
      )}
    </div>
  );
};

export default Schedule;
