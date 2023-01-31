// // import React from 'react'

// // function RiderMap() {
// //   return (
// //     <div>RiderMap</div>
// //   )
// // }

// // export default RiderMap



// //import the Google Maps React Component 
// import { GoogleMap, withScriptjs, withGoogleMap, DirectionsRenderer } from "react-google-maps";

// // define the function that will take in the current location and the destination and then return the necessary data to render the directions
// // const RiderMap = ({token,islogged}) => {
// const RiderMap = () => {
  
//   const { currentLocation, destination } = props;
//   currentLocation.lat=10
//   currentLocation.lng=76.5
  
//   destination.lat=12
//   destination.lng=78.5


//   // create a DirectionsService object 
//   const DirectionsService = new window.google.maps.DirectionsService();

//   // define the route object
//   const route = {
//     origin: new window.google.maps.LatLng(currentLocation.lat, currentLocation.lng),
//     destination: new window.google.maps.LatLng(destination.lat, destination.lng),
//     travelMode: window.google.maps.TravelMode.DRIVING
//   };
  
//   // define the function that will be called once the directions service returns the results
//   const onLoadDirections = (result, status) => {
//     if (status === window.google.maps.DirectionsStatus.OK) {
//       // set the directions result on the state
//       props.setDirections(result);
//     } else {
//       // set an error message
//       props.setErrorMessage(
//         `There was an error retrieving the directions: ${result}`
//       );
//     }
//   };
  
//   // call the DirectionsService with the route object and the callback function
//   DirectionsService.route(route, onLoadDirections);
  
//   // return the GoogleMap component that will render the directions
//   return (
//      <GoogleMap
//         defaultZoom={7}
//         defaultCenter={new window.google.maps.LatLng(currentLocation.lat, currentLocation.lng)}
//       >
//         {props.directions && (
//           <DirectionsRenderer
//             directions={props.directions}
//           />
//         )}
//       </GoogleMap>
//   );
// };

// // define the function that will be used to wrap the Directions component
// // const WrappedDirections = withScriptjs(withGoogleMap(Directions));

// // return the WrappedDirections component
// // return (
// //   <WrappedDirections
// //     currentLocation={this.state.currentLocation}
// //     destination={this.state.destination}
// //     setDirections={this.setDirections}
// //     setErrorMessage={this.setErrorMessage}
// //     // googleMapURL={`https://maps.googleapis.com/maps/api/js?key=${process.env.REACT_APP_GOOGLE_KEY}&v=3.exp&libraries=geometry,drawing,places`}
// //     googleMapURL={`https://maps.googleapis.com/maps/api/js?key=${process.env.REACT_APP_GOOGLE_KEY}&v=3.exp&libraries=geometry,drawing,places`}
// //     loadingElement={<div style={{ height: `100%` }} />}
// //     containerElement={<div style={{ height: `400px` }} />}
// //     mapElement={<div style={{ height: `100%` }} />}
// //   />
// // );

// export default RiderMap
