//import necessary components
import React, { useState } from "react";
import { Map, GoogleApiWrapper, Marker, DirectionsRenderer } from 'google-maps-react';
 
const RiderMap2 = (props) => {
  const [directions, setDirections] = useState(null);
 
  //function to get direction from current position to Kochi
  const getDirections = () => {
    const directionsService = new props.google.maps.DirectionsService();
    directionsService.route({
    //   origin: new props.google.maps.LatLng(props.currentLat, props.currentLng),
      origin: new props.google.maps.LatLng(10, 77),
      destination: new props.google.maps.LatLng(9.9312, 76.2673),
      travelMode: props.google.maps.TravelMode.DRIVING,
    }, (result, status) => {
      if (status === props.google.maps.DirectionsStatus.OK) {
        setDirections(result);
      } else {
        console.error(`error fetching directions ${result}`);
      }
    });
  }
 
  return (
    <Map
      google={props.google}
      zoom={14}
      initialCenter={{
        lat: props.currentLat,
        lng: props.currentLng
      }}
    >
      {/* <Marker
        position={{ lat: props.currentLat, lng: props.currentLng }}
      />
      <Marker
        position={{ lat: 9.9312, lng: 76.2673}}
      /> */}
      {/* <button onClick={getDirections}>Get Directions</button> */}
      {/* {directions && <DirectionsRenderer directions={directions} />} */}
    </Map>
  );
}
 
export default GoogleApiWrapper({
  apiKey: 'AIzaSyC-BWemSByl9AoF7KNOzaFDL503NNrjB_g'
})(RiderMap2);