import React, { useState } from "react";
import config from "../config";
import { useNavigate } from "react-router-dom";
import useAuthStore from "../store/authStore";
import { Button, Stack, TextField, Typography } from "@mui/material";

function SignIn() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const setUser = useAuthStore((state) => state.setUser); // Get setUid from the store
  const navigate = useNavigate();

  const handleSignIn = async (e) => {
    e.preventDefault();
    const response = await fetch(`${config.backendUrl}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    const data = await response.json();
    if (response.ok) {
      setUser(data.uid, username);
      setMessage(data.message);
      navigate("/");
    } else {
      setMessage(data.error || "Login failed.");
    }
  };

  return (
    <Stack gap={3} width={500}>
      <Typography variant="h5" sx={{ textAlign: "start" }}>
        Sign In
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
      <Typography
        sx={{
          textDecoration: "underline",
          textAlign: "end",
          cursor: "pointer",
        }}
        onClick={() => {
          navigate("/register/");
        }}
      >
        No account? Register
      </Typography>
      <Button
        type="submit"
        onClick={handleSignIn}
        sx={{
          boxShadow: "2px 2px 8px 1px rgba(0, 0, 0, 0.3)",
          "&:hover": {
            boxShadow: "4px 4px 10px 1px rgba(0, 0, 0, 0.4)",
          },
          color: "black",
        }}
      >
        Sign In
      </Button>

      <Typography>{message}</Typography>
    </Stack>
  );
}

export default SignIn;
