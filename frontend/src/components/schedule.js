import React, { useState, useEffect } from 'react';
import './schedule.css';

const Schedule = () => {
  const [fadeIn, setFadeIn] = useState(false);

  useEffect(() => {
      setFadeIn(true);
  }, []);
  
  return (
      <div className="schedule">
        <h1>Schedule</h1>
      </div>
  );
}

export default Schedule;
