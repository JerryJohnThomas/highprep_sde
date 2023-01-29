import React, { useState, useEffect } from 'react';
import { GoogleMap, withScriptjs, withGoogleMap, DirectionsRenderer } from 'react-google-maps';

function Map() {
  const [directions, setDirections] = useState(null);
  const [currentPosition, setCurrentPosition] = useState(null);

  useEffect(() => {
    navigator.geolocation.getCurrentPosition(position => {
      setCurrentPosition({
        lat: position.coords.latitude,
        lng: position.coords.longitude,
      });
    });
  }, []);

  useEffect(() => {
    const destination = { lat: 9.9312, lng: 76.2673 };
    const directionsService = new window.google.maps.DirectionsService();
    if (currentPosition) {
      directionsService.route(
        {
          origin: currentPosition,
          destination,
          travelMode: window.google.maps.TravelMode.DRIVING,
        },
        (result, status) => {
          if (status === window.google.maps.DirectionsStatus.OK) {
            setDirections(result);
          } else {
            console.error(`error fetching directions ${result}`);
          }
        }
      );
    }
  }, [currentPosition]);

  return (
    <GoogleMap
      defaultZoom={7}
      defaultCenter={currentPosition}
    >
      {directions && <DirectionsRenderer directions={directions} />}
    </GoogleMap>
  );
}

const WrappedMap = withScriptjs(withGoogleMap(Map));

export default function Directions() {
  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <WrappedMap
        googleMapURL={`https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&v=3.exp&libraries=geometry,drawing,places`}
        loadingElement={<div style={{ height: `100%` }} />}
        containerElement={<div style={{ height: `100%` }} />}
        mapElement={<div style={{ height: `100%` }} />}
      />
    </div>
  );
}
