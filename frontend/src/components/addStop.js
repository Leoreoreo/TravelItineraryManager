// AddStop.js
import React, { useState } from 'react';

const AddStop = ({ onSave, onCancel }) => {
  const [tripStop, setTripStop] = useState({ name: '', description: '', date: '' });

  const handleSave = () => {
    onSave(tripStop); // Call the onSave function passed from the parent
    setTripStop({ name: '', description: '', date: '' }); // Reset the input fields
  };

  return (
    <div className="modal-content">
      <h2>Add Trip Stop</h2>
      <label>
        Name:
        <input
          type="text"
          value={tripStop.name}
          onChange={(e) => setTripStop({ ...tripStop, name: e.target.value })}
        />
      </label>
      <label>
        Description:
        <input
          type="text"
          value={tripStop.description}
          onChange={(e) => setTripStop({ ...tripStop, description: e.target.value })}
        />
      </label>
      <label>
        Date:
        <input
          type="date"
          value={tripStop.date}
          onChange={(e) => setTripStop({ ...tripStop, date: e.target.value })}
        />
      </label>
      <button onClick={handleSave}>Save</button>
      <button onClick={onCancel}>Cancel</button>
    </div>
  );
};

export default AddStop;
