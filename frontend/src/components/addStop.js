import {
  Box,
  FormControl,
  Grid2,
  MenuItem,
  Select,
  TextField,
} from "@mui/material";
import React, { useState, useEffect } from "react";

const AddStop = ({ onAdd, onEdit, onCancel, initialData }) => {
  const [tripStop, setTripStop] = useState({
    title: "",
    type: "",

    startDate: "",
    startHour: "",
    startMinute: "",
    endDate: "",

    endHour: "",
    endMinute: "",
    location: "",
    link: "",
    description: "",
  });

  useEffect(() => {
    if (initialData) {
      setTripStop(initialData); // Pre-fill fields if editing
      console.log("initial data is ", initialData);
    }
  }, [initialData]);

  const handleAdd = () => {
    onAdd(tripStop);
    setTripStop({
      title: "",
      type: "",

      startDate: "",
      startHour: "",
      startMinute: "",
      endDate: "",

      endHour: "",
      endMinute: "",
      location: "",
      link: "",
      description: "",
    });
  };

  const handleEdit = () => {
    onEdit(tripStop);
    setTripStop({
      title: "",
      type: "",

      startDate: "",
      startHour: "",
      startMinute: "",
      endDate: "",

      endHour: "",
      endMinute: "",
      location: "",
      link: "",
      description: "",
    });
  };

  const OptionWrapper = ({ children }) => {
    return (
      <label
        className="event-option"
        style={{ display: "flex", gap: "3px", alignItems: "center" }}
      >
        {children}
      </label>
    );
  };

  return (
    <div
      className="event-modal"
      style={{ display: "flex", flexDirection: "column", gap: "5px" }}
    >
      <h2>{initialData ? "Edit Trip Stop" : "Add Trip Stop"}</h2>
      <div className="modal-content" style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
        <Grid2 container spacing={2}>
          <Grid2 size={6} sx={{ display: "flex", alignItems: "center" }}>
            <OptionWrapper>
              <div>Title:</div>
              <TextField
                hiddenLabel
                fullWidth
                type="text"
                size="small"
                value={tripStop.title}
                onChange={(e) =>
                  setTripStop({ ...tripStop, title: e.target.value })
                }
              />
            </OptionWrapper>
          </Grid2>
          <Grid2 size={6} sx={{ display: "flex", alignItems: "center" }}>
            <OptionWrapper>
              <div>Type:</div>

              <FormControl sx={{ m: 1, minWidth: 120 }}>
                <Select
                  value={tripStop.type}
                  onChange={(e) =>
                    setTripStop({ ...tripStop, type: e.target.value })
                  }
                  size="small"
                  displayEmpty
                >
                  <MenuItem value="">
                    <em>None</em>
                  </MenuItem>
                  <MenuItem value={"restaurants"}>Restaurants</MenuItem>
                  <MenuItem value={"hotels"}>Hotels & Accommodations</MenuItem>
                  <MenuItem value={"transportation"}>
                    Transportation Hubs
                  </MenuItem>
                  <MenuItem value={"attractions"}>
                    Landmarks & Attractions
                  </MenuItem>
                  <MenuItem value={"outdoor"}>Outdoor Activities</MenuItem>
                  <MenuItem value={"shopping"}>Shopping</MenuItem>
                  <MenuItem value={"entertainment"}>Entertainment</MenuItem>
                  <MenuItem value={"utilities"}>
                    Utilities & Essentials
                  </MenuItem>
                  <MenuItem value={"special"}>Special Stops</MenuItem>
                </Select>
              </FormControl>
            </OptionWrapper>
          </Grid2>
        </Grid2>

        <Grid2 container spacing={2}>
          <Grid2 size={6}>
            <div>Start Date:</div>
            <TextField
              hiddenLabel
              fullWidth
              type="date"
              size="small"
              value={tripStop.startDate}
              onChange={(e) =>
                setTripStop({ ...tripStop, startDate: e.target.value })
              }
            />
            <Box sx={{ display: "flex", alignItems: "center" }}>
              <TextField
                hiddenLabel
                fullWidth
                placeholder="Hour"
                type="text"
                size="small"
                value={tripStop.startHour}
                onChange={(e) =>
                  setTripStop({ ...tripStop, startHour: e.target.value })
                }
              />
              <TextField
                hiddenLabel
                fullWidth
                placeholder="Minute"
                type="text"
                size="small"
                value={tripStop.startMinute}
                onChange={(e) =>
                  setTripStop({ ...tripStop, startMinute: e.target.value })
                }
              />
            </Box>
          </Grid2>
          <Grid2 size={6}>
            <div>End Date:</div>
            <TextField
              hiddenLabel
              fullWidth
              type="date"
              size="small"
              value={tripStop.endDate}
              onChange={(e) =>
                setTripStop({ ...tripStop, endDate: e.target.value })
              }
            />
            <Box sx={{ display: "flex", alignItems: "center" }}>
              <TextField
                hiddenLabel
                fullWidth
                placeholder="Hour"
                type="text"
                size="small"
                value={tripStop.endHour}
                onChange={(e) =>
                  setTripStop({ ...tripStop, endHour: e.target.value })
                }
              />
              <TextField
                hiddenLabel
                fullWidth
                placeholder="Minute"
                type="text"
                size="small"
                value={tripStop.endMinute}
                onChange={(e) =>
                  setTripStop({ ...tripStop, endMinute: e.target.value })
                }
              />
            </Box>
          </Grid2>
        </Grid2>

          <div>Location:</div>
          <TextField
            hiddenLabel
            fullWidth
            type="text"
            size="small"
            value={tripStop.location}
            onChange={(e) =>
              setTripStop({ ...tripStop, location: e.target.value })
            }
          />

          Description:
          <TextField
            hiddenLabel
            fullWidth
            multiline
            rows={4}
            type="text"
            size="small"
            value={tripStop.description}
            onChange={(e) =>
              setTripStop({ ...tripStop, description: e.target.value })
            }
            placeholder="Type some description here..."
          />
      </div>
      <div style={{marginTop: "10px"}}>
        {initialData ? (
          <button onClick={handleEdit}>Save Changes</button>
        ) : (
          <button onClick={handleAdd}>Add</button>
        )}
        <button onClick={onCancel}>Cancel</button>
      </div>
    </div>
  );
};

export default AddStop;
