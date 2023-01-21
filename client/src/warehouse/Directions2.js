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
import RiderCard from './RiderCard'

// const center = { lat: 48.8584, lng: 2.2945 }
const center = { lat: 9.95, lng: 76.25 }

function Directions2() {


    const [rider_places, setRiderplaces] = useState([])
    const [renderitem, setRenderitem] = useState([])

    // const colors=["yellow", "red" , "blue"]
    const colors = [  "#A0E6FF",  "#FF8A80",  "#A4D3EE",  "#FFA07A",  "#90CAF9",  "#FF6347",  "#81D4FA",  "#FF7F50",  "#7FC4FD",  "#FF4500"]
  useEffect(()=>{

    setRiderplaces([
        [{rider_id: 1},{lat : 10.7992017 , lng:76.8221794},{lat:13.7992017 , lng:77.8221794}, {lat:12.5992017 , lng:76.9221794}, {lat:12.7992017 , lng:77.8221794}],
        [{rider_id: 2},{lat : 10.9992017 , lng:76.9221794}, {lat:12.6992017 , lng:77.5221794}],
    ])
},[])

    useEffect(()=>
    {
        if(window.google)
            console.log("window.google is up")
        else
        {
            console.log("window.google is not up")
            return;
        }


        console.log(rider_places)

        for (let index in rider_places )
        {
            let data = rider_places[index]
            let data_transformed = []
            
            let rider_id = data[0]["rider_id"];
            data.shift();
            console.log("rider " + rider_id+ " with " + data.length +" points ");
            
            
            // eslint-disable-next-line no-undef
            for(let i=0;i<data.length;i++)
            {
                let temp = new window.google.maps.LatLng(data[i].lat, data[i].lng);
                data_transformed.push(temp);
            }
            
            let origin = data_transformed[0];
            let waypoints_temp = data_transformed.slice(1, data_transformed.length - 1)
            let waypoints = []
            for (let ind3 in waypoints_temp)
                waypoints.push({location:waypoints_temp[ind3]})
            let destination = data_transformed[data_transformed.length-1];

            // console.log("origin")
            // console.log(origin)
            // console.log("waypoints")
            // console.log(waypoints)
            // console.log("destination")
            // console.log(destination)

            let res = calculateRouteTuples(origin, waypoints, destination)
            console.log("returned calculated routes")

        }

    },[rider_places,window.google])

  
  const { isLoaded } = useJsApiLoader({
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
  async function calculateRouteTuples(org, wp, dest) {
   
    const directionsService = new window.google.maps.DirectionsService()
    const results = await directionsService.route({
      origin: org,
      waypoints : wp,
      destination: dest,
      // eslint-disable-next-line no-undef
      travelMode: google.maps.TravelMode.DRIVING,
    })

    setRenderitem( renderitem => [...renderitem, results])
    setDirectionsResponse(results)

    // setDistance(results.routes[0].legs[0].distance.text)
    // setDuration(results.routes[0].legs[0].duration.text)
    console.log("over");
    return "okk";
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
          {
              renderitem.map((data,index) => {
                return(
                    <div>
                        <DirectionsRenderer directions={data} options={{polylineOptions:{strokeColor:colors[index]}}} />
                    </div>
                )
                }
            )
          }

        </GoogleMap>
        </div>


        <div className='jerry_directions2_rider_info'>
          {
            renderitem.map((data,index)=>(
                <RiderCard />
            ))
          }

        </div>

        </div>
        </>

  )
}

export default Directions2