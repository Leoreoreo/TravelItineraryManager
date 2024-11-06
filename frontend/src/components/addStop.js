import React, { useState, useEffect } from 'react';

const AddStop = ({ onAdd, onEdit, onCancel, initialData }) => {
  const [tripStop, setTripStop] = useState({
    title: '',
    type: '',

    startDate: '',
    startHour: '',
    startMinute: '',
    endDate: '',

    endHour: '',
    endMinute: '',
    location: '',
    link: '',
    description: ''
  });

  useEffect(() => {
    if (initialData) {
      setTripStop(initialData); // Pre-fill fields if editing
      console.log("initial data is ", initialData)
    }
  }, [initialData]);

  const handleAdd = () => {
    onAdd(tripStop);
    setTripStop({
      title: '',
      type: '',

      startDate: '',
      startHour: '',
      startMinute: '',
      endDate: '',

      endHour: '',
      endMinute: '',
      location: '',
      link: '',
      description: ''
    });
  };

  const handleEdit = () => {
    onEdit(tripStop);
    setTripStop({
      title: '',
      type: '',

      startDate: '',
      startHour: '',
      startMinute: '',
      endDate: '',

      endHour: '',
      endMinute: '',
      location: '',
      link: '',
      description: ''
    });
  };

  return (
    <div className="modal-content">
      <h2>{initialData ? 'Edit Trip Stop' : 'Add Trip Stop'}</h2>
      <label>
        Title:
        <input
          type="text"
          value={tripStop.title}
          onChange={(e) => setTripStop({ ...tripStop, title: e.target.value })}
        />
      </label>
      <label>
        Type:
        <input
          type="text"
          value={tripStop.type}
          onChange={(e) => setTripStop({ ...tripStop, type: e.target.value })}
        />
      </label>
      <label>
        Start Date:
        <input
          type="date"
          value={tripStop.startDate}
          onChange={(e) => setTripStop({ ...tripStop, startDate: e.target.value })}

        />
      </label>
      <label>
        Start Time:
        <input
          type="number"
          placeholder="Hour"
          value={tripStop.startHour}
          onChange={(e) => setTripStop({ ...tripStop, startHour: e.target.value })}
        />
        <input
          type="number"
          placeholder="Minute"
          value={tripStop.startMinute}
          onChange={(e) => setTripStop({ ...tripStop, startMinute: e.target.value })}
        />
      </label>
      <label>
        End Date:
        <input
          type="date"
          value={tripStop.endDate}
          onChange={(e) => setTripStop({ ...tripStop, endDate: e.target.value })}
        />
      </label>
      <label>
        End Time:
        <input
          type="number"
          placeholder="Hour"
          value={tripStop.endHour}
          onChange={(e) => setTripStop({ ...tripStop, endHour: e.target.value })}
        />
        <input
          type="number"
          placeholder="Minute"
          value={tripStop.endMinute}
          onChange={(e) => setTripStop({ ...tripStop, endMinute: e.target.value })}
        />
      </label>
      <label>
        Location:
        <input
          type="text"
          value={tripStop.location}
          onChange={(e) => setTripStop({ ...tripStop, location: e.target.value })}
        />
      </label>
      <label>
        Link:
        <input
          type="url"
          value={tripStop.link}
          onChange={(e) => setTripStop({ ...tripStop, link: e.target.value })}
        />
      </label>
      <label>
        Description:
        <textarea
          value={tripStop.description}
          onChange={(e) => setTripStop({ ...tripStop, description: e.target.value })}
        />
      </label>
      {initialData ? <button onClick={handleEdit}>Save Changes</button> : <button onClick={handleAdd}>Add</button>}
      <button onClick={onCancel}>Cancel</button>
    </div>
  );
};

export default AddStop;