
import React, { useState, useEffect } from "react";
import { GoogleMap, DirectionsRenderer, LoadScript } from "@react-google-maps/api";
import "./GoogleMapsDirections.css"

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

//   useEffect(() => {
//   const script = document.createElement('script');
//   script.src = 'https://apis.google.com/js/api.js';
//   script.async = true;
//   script.defer = true;
//   script.onload = () => {
//     window.google.load('picker', '1', { callback: the_magic_do_it_all_function });
//   };
//   document.body.appendChild(script);
// }, []);
 
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
            if (status === window.google.maps.DirectionsStatus.OK) {
              console.log(result);
              console.log(result.length);
            console.log(result.routes[0].legs[0].steps)
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
  
    <div className="gmd_left">
      <LoadScript
      googleMapsApiKey="AIzaSyC-BWemSByl9AoF7KNOzaFDL503NNrjB_g"
    >
      <GoogleMap
        mapContainerStyle={{
        // height: "800px",
        height:"100%",
        width:"100%",
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
    </div>

    <div className="gmd_right">

    <div className="gmd_right_title">Route Info</div>
    {directions && directions.routes[0].legs[0].steps.map((data,index)=>
      <DirectionCard data={data} index={index} />
    )}
    </div>
    
    </div>
  );
};
 

const DirectionCard = ({data,index})=>{
  return (
    <div className="DirectionCard_container">
      <div>Distance: {data.distance.text} Time : {data.duration.text}</div>
      <div dangerouslySetInnerHTML={{ __html: data.instructions }} />
    </div>
  )
}
export default GoogleMapsDirections;