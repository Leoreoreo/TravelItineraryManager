import React, { useState, useEffect } from 'react';
import GoogleMap from './googleMap';
import AddStop from './addStop';

const Schedule = () => {
  const [fadeIn, setFadeIn] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [tripStops, setTripStops] = useState([]); // State to hold the trip stops
  const [editingStop, setEditingStop] = useState(null); // State to track the stop being edited

  useEffect(() => {
    setFadeIn(true);
  }, []);

  const handleAddClick = () => {
    setEditingStop(null); // Reset editingStop when adding a new stop
    setShowModal(true);
  };

  const handleSaveTripStop = (stop) => {
    if (editingStop !== null) {
      // Update existing stop
      setTripStops(tripStops.map((s, index) => (index === editingStop ? stop : s)));
    } else {
      // Add new stop
      setTripStops([...tripStops, stop]);
    }
    setShowModal(false);
  };

  const handleEditTripStop = (index) => {
    setEditingStop(index);
    setShowModal(true);
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
            <div
              key={index}
              className="trip-stop-card"
              onClick={() => handleEditTripStop(index)}
            >
              <h2>{stop.title}</h2>
              <p><strong>Type:</strong> {stop.type}</p>
              <p>
                <strong>Time Slot:</strong> {stop.date} - {stop.startHour}:{stop.startMinute} to {stop.endHour}:{stop.endMinute}
              </p>
              <p><strong>Location:</strong> {stop.location}</p>
              {stop.link && (
                <p>
                  <strong>Link:</strong> <a href={stop.link} target="_blank" rel="noopener noreferrer">{stop.link}</a>
                </p>
              )}
              <p><strong>Description:</strong> {stop.description}</p>
            </div>
          ))}
        </div>
      </div>

      {showModal && (
        <div className="modal">
          <AddStop
            onSave={handleSaveTripStop}
            onCancel={() => setShowModal(false)}
            initialData={editingStop !== null ? tripStops[editingStop] : null} // Pass the stop to edit or null
          />
        </div>
      )}
    </div>
  );
};

export default Schedule;
