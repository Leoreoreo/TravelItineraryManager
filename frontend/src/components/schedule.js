// Schedule.js
import React, { useState, useEffect } from 'react';
import GoogleMap from './googleMap';
import AddStop from './addStop'; // Import the AddStop component

const Schedule = () => {
  const [fadeIn, setFadeIn] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [tripStops, setTripStops] = useState([]); // State to hold the trip stops

  useEffect(() => {
    setFadeIn(true);
  }, []);

  const handleAddClick = () => {
    setShowModal(true); // Open the modal when "Add" is clicked
  };

  const handleSaveTripStop = (newStop) => {
    setTripStops([...tripStops, newStop]); // Append the new trip stop
    setShowModal(false); // Close the modal after saving
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
              <strong>{stop.name}</strong> - {stop.description} on {stop.date}
            </li>
          ))}
        </ul>
      </div>

      {showModal && (
        <div className="modal">
          <AddStop onSave={handleSaveTripStop} onCancel={() => setShowModal(false)} />
        </div>
      )}
    </div>
  );
};

export default Schedule;
