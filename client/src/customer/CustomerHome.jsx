import useGeolocation from "react-hook-geolocation";
import { useMemo } from "react";
import { GoogleMap, useLoadScript, Marker } from "@react-google-maps/api";

function CustomerHome({ token, islogged }) {
    const { isLoaded } = useLoadScript({
        googleMapsApiKey: "AIzaSyC-BWemSByl9AoF7KNOzaFDL503NNrjB_g",
    });

    if (!isLoaded) return <div>Loading...</div>;
    return <Map />;
}

function Map() {
  const location = useGeolocation();
  const center = useMemo(() => ({ lat:location.latitude , lng: location.longitude }), []);
  console.log(location);
  return (
    <GoogleMap zoom={10} center={center} mapContainerClassName="map-container">
      <Marker position={center} />
    </GoogleMap>
  );

//   return !geolocation.error ? (
//     <ul>
//       <li>Latitude: {geolocation.latitude}</li>
//       <li>Longitude: {geolocation.longitude}</li>
//       <li>Location accuracy: {geolocation.accuracy}</li>
//       <li>Altitude: {geolocation.altitude}</li>
//       <li>Altitude accuracy: {geolocation.altitudeAccuracy}</li>
//       <li>Heading: {geolocation.heading}</li>
//       <li>Speed: {geolocation.speed}</li>
//       <li>Timestamp: {geolocation.timestamp}</li>
//     </ul>
//   ) : (
//     <p>No geolocation, sorry.</p>
//   );
};

export default CustomerHome;