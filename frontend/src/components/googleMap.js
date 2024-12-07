import React, { useState, useCallback, useEffect, useMemo } from 'react';
import { GoogleMap, useJsApiLoader, DirectionsService, DirectionsRenderer } from '@react-google-maps/api';
import { Box, CircularProgress, Typography } from '@mui/material';

// Define Google Maps options with useMemo to avoid recreating the object
const MapComponent = ({ commuteArray }) => {
    const googleMapsOptions = useMemo(() => ({
        googleMapsApiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY,
        libraries: ['places'],
    }), []); // Empty dependency array to keep it stable across renders

    const { isLoaded } = useJsApiLoader(googleMapsOptions);
    const [directions, setDirections] = useState([]);
    
    const getTravelMode = (vehicle) => {
        switch (vehicle) {
            case 'walk':
                return window.google.maps.TravelMode.WALKING;
            case 'car':
                return window.google.maps.TravelMode.DRIVING;
            case 'subway':
                return window.google.maps.TravelMode.TRANSIT;
            default:
                return window.google.maps.TravelMode.DRIVING;
        }
    };

    const calculateRoutes = useCallback(() => {
        if (!commuteArray || commuteArray.length === 0) return;

        const newDirections = [];
        const directionsService = new window.google.maps.DirectionsService();

        commuteArray.forEach((commute, index) => {
            if (commute.vehicle === 'flight') return; // Ignore flights

            directionsService.route(
                {
                    origin: commute.start_location,
                    destination: commute.end_location,
                    travelMode: getTravelMode(commute.vehicle),
                },
                (result, status) => {
                    if (status === window.google.maps.DirectionsStatus.OK) {
                        newDirections[index] = result; // Save result in the same index
                        setDirections([...newDirections]); // Update state with new directions
                    } else {
                        console.error(`Error fetching directions for index ${index}: ${result}`);
                    }
                }
            );
        });
    }, [commuteArray]);

    // Trigger route calculations once map is loaded
    useEffect(() => {
        if (isLoaded) {
            calculateRoutes();
        }
    }, [isLoaded, calculateRoutes]);

    return isLoaded ? (
        <div className="googleMap">
            <GoogleMap
                mapContainerStyle={{ width: '100%', height: '100%' }}
                center={{ lat: 40.7128, lng: -74.0060 }}
                zoom={8}
            >
                {directions.map((direction, idx) => 
                    direction && <DirectionsRenderer key={idx} directions={direction} />
                )}
            </GoogleMap>
        </div>
    ) : (
        <Box sx={{display: "flex", flexDirection:"column", justifyContent:"center", alignItems: "center", height: "90vh"}}>
            <Typography>Loading the map</Typography>
            <CircularProgress />
        </Box>
    );
};

export default MapComponent;
