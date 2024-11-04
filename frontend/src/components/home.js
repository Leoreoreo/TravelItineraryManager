import {
  Box,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  TextField,
  Typography,
} from "@mui/material";
import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import useAuthStore from "../store/authStore";
import useTripStore from "../store/tripStore";

const Home = ({ user }) => {
  const [activeLink, setActiveLink] = useState("/");
  const [open, setOpen] = useState(false);
  const [title, setTitle] = useState("");
  const [message, setMessage] = useState("");
  const uid = useAuthStore((state) => state.uid);
  const { trips, loading, error, fetchTrips, addTrip, removeTrip } = useTripStore();

  useEffect(() => {
    setActiveLink("/");
  }, []);

  useEffect(() => {
    if (uid && trips.length === 0) {
      fetchTrips(uid);
    }
  }, [uid]);

  const handleOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleAddTrip = async () => {
    if (title.trim().length === 0) {
      setMessage("please enter the title");
      return;
    }
    if (!uid) {
      setMessage("please login first");
      return;
    }

    setMessage("");

    await addTrip(uid, title, null, null); // later need to add start date and end date
    if (error) {
      setMessage(error);
    } else {
      setTitle("");
      handleClose();
    }
  };

  const handleDelete = (trip_id) => {
    removeTrip(trip_id)
  }

  return (
    <div>
      <br />
      <div>
        <h1>Welcome, {user}! </h1>
        <br />
        <br />
        <br />
        {trips &&
          trips.map(({ trip_id, trip_name, start_date, end_date }) => (
            <h2 className="trips" key={trip_id}>
              <Link
                to={`/trip/${trip_id}`}
                className={activeLink === `/trip/${trip_id}` ? "active" : ""}
                onClick={() => setActiveLink(`/trip/${trip_id}`)}
              >
                {trip_name}
              </Link>
              <button className="delete-trip-button" onClick={()=>handleDelete(trip_id)}>x</button>
            </h2>
          ))}
        <br />
        <br />
        <br />
        <h2>
          <Button onClick={handleOpen}>Add Trip</Button>
        </h2>
      </div>

      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Start a new trip!</DialogTitle>
        <DialogContent>
          <Box sx={{ display: "flex", gap: 3, alignItems: "center" }}>
            <Typography variant="h6">Title:</Typography>
            <TextField
              hiddenLabel
              size="small"
              value={title}
              onChange={(event) => setTitle(event.target.value)}
            />
          </Box>
          {message.length !== 0 && (
            <Typography variant="h6" color="red">
              {message}
            </Typography>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleAddTrip} autoFocus>
            Add
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
};

export default Home;
