import React, { useState } from "react";
import config from "../config";
import { useNavigate } from "react-router-dom";
import { Button, Stack, TextField, Typography } from "@mui/material";

function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    const response = await fetch(`${config.backendUrl}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    const data = await response.json();
    if (response.ok) {
      setMessage(data.message);
      navigate("/signin/");
    } else {
      setMessage(data.error || "Registration failed.");
    }
  };

  return (
    <Stack gap={3} width={500}>
      <Typography variant="h5" sx={{ textAlign: "start" }}>
        Register
      </Typography>
      <TextField
        hiddenLabel
        fullWidth
        placeholder="Enter user name"
        size="small"
        type="text"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        required
      />
      <TextField
        hiddenLabel
        fullWidth
        placeholder="Password"
        size="small"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
      <Button
        type="submit"
        onClick={handleRegister}
        sx={{
          boxShadow: "2px 2px 8px 1px rgba(0, 0, 0, 0.3)",
          "&:hover": {
            boxShadow: "4px 4px 10px 1px rgba(0, 0, 0, 0.4)",
          },
          color: "black",
        }}
      >
        Register
      </Button>

      <Typography>{message}</Typography>
    </Stack>
  );
}

export default Register;
