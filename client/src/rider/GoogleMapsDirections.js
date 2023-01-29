
import React, { useState, useEffect } from "react";
import { GoogleMap, DirectionsRenderer, LoadScript } from "@react-google-maps/api";
const GoogleMapsDirections = () => {
  const [directions, setDirections] = useState(null);
 
  useEffect(() => {

    if(!window.google)
        return;

    const directionsService = new window.google.maps.DirectionsService();
    navigator.geolocation.getCurrentPosition(position => {
      const start = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };
      const end = {
        lat: 10.015,
        lng: 76.34
      };
      directionsService.route(
        {
          origin: start,
          destination: end,
          travelMode: window.google.maps.TravelMode.DRIVING
        },
        (result, status) => {
            console.log("res");
            console.log(result);
          if (status === window.google.maps.DirectionsStatus.OK) {
            setDirections(result);
          } else {
            console.error(`error fetching directions ${result}`);
          }
        }
      );
    });
  },[window.google]);
 
  return (
    <div className="gmd_container">
    {/*
     <GoogleMap
      id="direction-example"
      mapContainerStyle={{
        height: "400px",
        width: "400px"
      }}
      zoom={7}
      center={{
        lat: 41.8507300,
        lng: -87.6512600
      }}
    >
      {directions && <DirectionsRenderer directions={directions} />}
    </GoogleMap> 
    */}

    <LoadScript
      googleMapsApiKey="AIzaSyC-BWemSByl9AoF7KNOzaFDL503NNrjB_g"
    >
      <GoogleMap
        mapContainerStyle={{
        height: "800px",
        width: "800px"
      }}
        center={{
        lat: 41.8507300,
        lng: -87.6512600
      }}
        zoom={10}
      >
          {directions && <DirectionsRenderer directions={directions} />}
      </GoogleMap>
    </LoadScript>

    <div>gmd</div>

    
    </div>
  );
};
 
export default GoogleMapsDirections;