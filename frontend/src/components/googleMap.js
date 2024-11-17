import React, { useState, useCallback, useEffect, useMemo } from 'react';
import { GoogleMap, useJsApiLoader, DirectionsService, DirectionsRenderer } from '@react-google-maps/api';

// Define Google Maps options with useMemo to avoid recreating the object
const MapComponent = ({ addresses }) => {
    const googleMapsOptions = useMemo(() => ({
        googleMapsApiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY,
        libraries: ['places'],
    }), []); // Empty dependency array to keep it stable across renders

    const { isLoaded } = useJsApiLoader(googleMapsOptions);
    const [directions, setDirections] = useState(null);

    // Memoize calculateRoute to avoid re-running it unnecessarily
    const calculateRoute = useCallback(() => {
        if (addresses.length < 2) return;

        const waypoints = addresses.slice(1, -1).map((address) => ({
            location: address,
            stopover: true,
        }));

        const directionsService = new window.google.maps.DirectionsService();
        directionsService.route(
            {
                origin: addresses[0],
                destination: addresses[addresses.length - 1],
                waypoints: waypoints,
                travelMode: window.google.maps.TravelMode.DRIVING,
            },
            (result, status) => {
                if (status === window.google.maps.DirectionsStatus.OK) {
                    console.log('Google Maps API response:', result);
                    setDirections(result);
                } else {
                    console.error(`Error fetching directions ${result}`);
                }
            }
        );
    }, [addresses]);

    // Only calculate the route once addresses are available
    useEffect(() => {
        if (isLoaded) {
            calculateRoute();
        }
    }, [isLoaded, calculateRoute]);

    return isLoaded ? (
        <div className="googleMap">
            <GoogleMap
                mapContainerStyle={{ width: '100%', height: '100%' }}
                center={{ lat: 40.7128, lng: -74.0060 }}
                zoom={8}
            >
                {directions && <DirectionsRenderer directions={directions} />}
            </GoogleMap>
        </div>
    ) : (
        <p>Loading...</p>
    );
};

export default MapComponent;
