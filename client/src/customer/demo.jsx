import { useMemo ,useState,useEffect} from "react";
import { GoogleMap, useLoadScript, MarkerF } from "@react-google-maps/api";
import useGeolocation from "react-hook-geolocation";
import "./demo.css"

export default function Demo() {
  const { isLoaded } = useLoadScript({
    googleMapsApiKey: "AIzaSyC-BWemSByl9AoF7KNOzaFDL503NNrjB_g",
  });

  if (!isLoaded) return <div>Loading...</div>;
  return <Map />;
}

function Map() {
  
  //const center = useMemo(() => ({ lat:parseFloat(location.latitude) , lng:parseFloat(location.longitude)  }), []);
  const[userLat, setUserLat]= useState(0);
const[userLong, setUserLong]= useState(0);

useEffect(()=> {
  navigator.geolocation.getCurrentPosition(position =>{
    setUserLat(position.coords.latitude);
    setUserLong(position.coords.longitude);
    console.log(userLat, userLong);
  })
},[]);
 console.log(userLat)
  const center =  {
    lat:userLat,
    lng:userLong
  }

  return (
<GoogleMap zoom={16} center={center} mapContainerClassName="map-container">
      <MarkerF position={center} />
    </GoogleMap>
  );
}