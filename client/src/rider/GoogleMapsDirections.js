
import React, { useState, useEffect } from "react";
import { GoogleMap, DirectionsRenderer, LoadScript } from "@react-google-maps/api";
const GoogleMapsDirections = () => {
  const [directions, setDirections] = useState(null);
 
  useEffect(() => {

    if(!window.google)
    {
      console.log("window google not loaded");
      return;
    }
    else
    {
      console.log("window google loaded");
      the_magic_do_it_all_function();
    }
  },[window.google]);

  useEffect(() => {
  const script = document.createElement('script');
  script.src = 'https://apis.google.com/js/api.js';
  script.async = true;
  script.defer = true;
  script.onload = () => {
    window.google.load('picker', '1', { callback: the_magic_do_it_all_function });
  };
  document.body.appendChild(script);
}, []);
 
  let the_magic_do_it_all_function = () =>{
    
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
            console.log(result.routes[0].legs[0].steps)
          if (status === window.google.maps.DirectionsStatus.OK) {
            setDirections(result);
          } else {
            console.error(`error fetching directions ${result}`);
          }
        }
      );
    });
  }

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
      <div>{directions.length}</div>
    <div>gmd</div>
      {
        
        directions.routes[0] && directions.routes[0].legs[0].steps.map((data,index)=>{
          <>
          <div>okk </div>
        <div>
            {index}
            {data.distance}
            {data.time}
            {data.instructions}
            </div>
          </>
        })
      }
    
    </div>
  );
};
 
export default GoogleMapsDirections;