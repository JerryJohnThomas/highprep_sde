import React from 'react'
import {
  withGoogleMap,
  Marker,
  GoogleMap,
  DirectionsRenderer
} from 'react-google-maps';
     
     

    let GoogleMapExample = withGoogleMap(props => (
      <GoogleMap
        defaultCenter={{ lat: 40.756795, lng: -73.954298 }}
        defaultZoom={13}
        center={this.state.currentLocation}
        onClick={this.onMapClick}
      >
        {this.state.centerMarker !== null && (
          <Marker position={this.state.centerMarker} label={'userloc'} />
        )}
        {this.state.markerPos !== null && (
          <Marker position={this.state.markerPos} />
        )}
        {this.state.directions !== null && (
          <DirectionsRenderer
            directions={this.state.directions}
            defaultOptions={{
              suppressMarkers: true
            }}
          />
        )}
      </GoogleMap>
    ));

function Directions() {
  return (
      <>
        <div>Directions</div>
      
        <div>
        <button onClick={this.getDirections}>Get Direction</button>
        <GoogleMapExample
          containerElement={<div style={{ height: `500px`, width: '500px' }} />}
          mapElement={<div style={{ height: `100%` }} />}
        />
      </div>
      </>
  )
}

export default Directions