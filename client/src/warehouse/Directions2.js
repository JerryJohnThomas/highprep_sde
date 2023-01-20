import {
  Box,
  Button,
  ButtonGroup,
  Flex,
  HStack,
  IconButton,
  Input,
  SkeletonText,
  Text,
} from '@chakra-ui/react'
import "./Directions.css"

import { FaLocationArrow, FaTimes } from 'react-icons/fa'

import {
  useJsApiLoader,
  GoogleMap,
  Marker,
  Autocomplete,
  DirectionsRenderer,
} from '@react-google-maps/api'
import { useRef, useState } from 'react'
import { useEffect } from 'react'
import { addScaleCorrector } from 'framer-motion'

// const center = { lat: 48.8584, lng: 2.2945 }
const center = { lat: 10, lng: 78 }

function Directions2() {

  // useEffect(()=>{
  //   console.log("use effect");
  //   let api_key = process.env.REACT_APP_GOOGLE_MAPS_API;
  //   console.log(api_key);
  // })

  
  const { isLoaded } = useJsApiLoader({
    // googleMapsApiKey: process.env.REACT_APP_GOOGLE_MAPS_API,
    googleMapsApiKey: 'AIzaSyC-BWemSByl9AoF7KNOzaFDL503NNrjB_g',
    libraries: ['places'],
  })

  const [map, setMap] = useState(/** @type google.maps.Map */ (null))
  const [directionsResponse, setDirectionsResponse] = useState(null)
  const [distance, setDistance] = useState('')
  const [curlat, setCurlat] = useState('')
  const [curlong, setCurlong] = useState('')
  const [duration, setDuration] = useState('')

  const originRef = useRef()
  const destiantionRef = useRef()
  const thirdplaceRef = useRef()

  if (!isLoaded) {
    return <div>not loaded</div>
  }


  async function getLocation () {
  if (!navigator.geolocation) {
    console.log("not supported")
  } else {
    console.log('Locating...')
    navigator.geolocation.getCurrentPosition((position) => {
      // this is not working 
      setCurlat(position.coords.latitude);
      setCurlong(position.coords.longitude);
      console.log(position.coords.latitude+ "  "+position.coords.longitude);
      return position.coords;
    }, () => {
    });
  }
}

  async function calculateRoute() {
    if (originRef.current.value === '' || destiantionRef.current.value === '') {
      return
    }

    getLocation().then((data)=>{
      console.log("over")
      console.log(curlat);
      console.log(data);
    })

    // eslint-disable-next-line no-undef
    const waypts = [
        // {location : new window.google.maps.LatLng(9.74, 121.05455)},
        // {location : new window.google.maps.LatLng(14.546748, 121.05455)},
        // {location : "Ernakulam"},
        // {location : "Madurai"},
        // {location : new window.google.maps.LatLng(9.74, 77.05455)},
        {location : new window.google.maps.LatLng(10.7992017 , 76.8221794)},
        // {location : new window.google.maps.LatLng(curlat, curlong)},
      ]

    const directionsService = new window.google.maps.DirectionsService()
    const results = await directionsService.route({
      origin: originRef.current.value,
      waypoints : waypts,
      destination: destiantionRef.current.value,
      // eslint-disable-next-line no-undef
      travelMode: google.maps.TravelMode.DRIVING,
    })


    setDirectionsResponse(results)
    setDistance(results.routes[0].legs[0].distance.text)
    setDuration(results.routes[0].legs[0].duration.text)
  }

  function clearRoute() {
    setDirectionsResponse(null)
    setDistance('')
    setDuration('')
    originRef.current.value = ''
    destiantionRef.current.value = ''
    thirdplaceRef.current.value = ''
  }

  return (
 <>
        <div className='jerry_directions2_contianer_top'>
        <div className='jerry_directions2_map_container'>
        <GoogleMap
          center={center}
          zoom={15}
          mapContainerStyle={{ width: '100%', height: '100%' }}
          options={{
              zoomControl: false,
              streetViewControl: false,
              mapTypeControl: false,
              fullscreenControl: false,
            }}
            onLoad={map => setMap(map)}
            >
          <Marker position={center} />
          {directionsResponse && (
              <DirectionsRenderer directions={directionsResponse} options={{polylineOptions:{strokeColor:"yellow"}}} />
              )}
          
        </GoogleMap>
        </div>


        <div className='jerry_directions2_rider_info'>
            Rider Component

        </div>

        </div>
        </>

  )
}

export default Directions2