import {
    Box,
    Button,
    ButtonGroup,
    Flex,
    HStack,
    IconButton,
    Input,
    list,
    SkeletonText,
    Text,
} from "@chakra-ui/react";
import "./Directions.css";

import { FaLocationArrow, FaTimes } from "react-icons/fa";
import axios from "../axios";
import {
    useJsApiLoader,
    GoogleMap,
    Marker,
    Autocomplete,
    DirectionsRenderer,
} from "@react-google-maps/api";
import { useRef, useState } from "react";
import { useEffect } from "react";
//import { addScaleCorrector } from 'framer-motion'
import RiderCard from "./RiderCard";
import UploadExcel_Pickup from "./UploadExcel_Pickup";
// import { Alert } from "@material-ui/core";
import { Alert } from "@mui/material";
// const center = { lat: 48.8584, lng: 2.2945 }
let center = { lat: 12.9716, lng: 77.5946 };
function Directions2({ setRandomNumber, randomNumber, token, islogged }) {
    const [showUpload, setShowUpload] = useState(false);
    const [uploadedExcel, setUploadedExcel] = useState(null);
    const [gotCenter, setGotCenter] = useState(false);
    const [gotCenterData, setGotCenterData] = useState([12.9716, 77.5946]);

    const [triggerUseEffect, setTriggerUseEffect] = useState(1);
    const [stats, setStats] = useState([]);
    const [showRiderRoute, setShowRiderRoute] = useState([]);
    const [rider_places, setRiderplaces] = useState([]);
    const [trigger_api, setTrigger_api] = useState(1);
    const [renderitem, setRenderitem] = useState([]);

    //metric states
    const [min_time_state, setMin_time_state] = useState(9999999);
    const [max_time_state, setMax_time_state] = useState(0);
    const [sum_time_state, setSum_time_state] = useState(0);

    const [min_dist_state, setMin_dist_state] = useState(9999999);
    const [max_dist_state, setMax_dist_state] = useState(0);
    const [sum_dist_state, setSum_dist_state] = useState(0);

    const [open, setOpen] = useState(false);

    let colors = [
        "yellow",
        "red",
        "blue",
        "green",
        "violet",
        "#394053",
        "#7CAE7A",
        "#553555",
        "#F06543",
        "#DC6BAD",
        "#F4AC32",
        "#89023E",
        "#643A71",
    ];
    // const colors = [  "#A0E6FF",  "#FF8A80",  "#A4D3EE",  "#FFA07A",  "#90CAF9",  "#FF6347",  "#81D4FA",  "#FF7F50",  "#7FC4FD",  "#FF4500"]

    let starter_fn = () => {
        console.log("starting Direction2 axiod useeffect");
        console.log("token", token);
        console.log("randomNumber", randomNumber);
        setMin_time_state(9999999);
        setMax_time_state(0);
        setSum_time_state(0);
        setMin_dist_state(9999999);
        setMax_dist_state(0);
        setSum_dist_state(0);

        axios
            .post(`/algo/status/`, {
                token: token,
                randomNumber: randomNumber,
                // "token": {lfe8m4uxkh},
                // "token": "33fc7ab5df252f5e197d8fbdb7f28a7d06421a5f",
                // "randomNumber" : "gutatlpv1o"
            })
            .then((res) => {
                console.log(res.data);
                if (
                    res.data.msg == "Algo is still going on" ||
                    res.data.msg == "started dynamic pickup points"
                ) {
                    setTimeout(() => {
                        setTriggerUseEffect((x) => x + 1);
                    }, 1000 * 15);
                    return;
                }

                setRiderplaces([]);
                setShowRiderRoute([]);
                let data = res.data;
                let rider_to_loc = data.rider_to_location;
                for (let i = 0; i < rider_to_loc.length; i++) {
                    let temp = [];
                    let rid = { rider_id: rider_to_loc[i].email };
                    let list_locations =
                        rider_to_loc[i].location_ids.coordinates;
                    temp.push(rid);

                    for (let j = 0; j < list_locations.length; j++) {
                        temp.push({
                            lat: list_locations[j][1],
                            lng: list_locations[j][2],
                        });
                    }
                    setRiderplaces((old) => [...old, temp]);
                    setShowRiderRoute((old) => [...old, true]);
                    setGotCenterData((x)=>[temp[temp.length-1].lat,temp[temp.length-1].lng]);
                    // console.log("center it", );
                    setGotCenter(true);
                    // console.log(center);
                }
                setTrigger_api((x) => x + 1);
                setOpen(true);
            })
            .catch((error) => {
                console.log(error);
            });
    };
    useEffect(() => {
        starter_fn();
        console.log("started function use Effect !!!!!!!!!!!! ");
        // setRiderplaces([
        //     [{rider_id: 1},{lat : 10.7992017 , lng:76.8221794},{lat:13.7992017 , lng:77.8221794}, {lat:12.5992017 , lng:76.9221794}, {lat:12.7992017 , lng:77.8221794}],
        //     [{rider_id: 2},{lat : 10.9992017 , lng:76.9221794}, {lat:12.6992017 , lng:77.5221794}],
        // ])
    }, [triggerUseEffect]);

    useEffect(() => {
        if (window.google) console.log("window.google is up");
        else {
            console.log("window.google is not up");
            return;
        }

        console.log(rider_places);

        for (let index in rider_places) {
            let data = rider_places[index];
            let data_transformed = [];

            let rider_id = data[0]["rider_id"];
            data.shift();

            // eslint-disable-next-line no-undef
            for (let i = 0; i < data.length; i++) {
                let temp = new window.google.maps.LatLng(
                    data[i].lat,
                    data[i].lng
                );
                data_transformed.push(temp);
            }

            let origin = data_transformed[0];
            let waypoints_temp = data_transformed.slice(
                1,
                data_transformed.length - 1
            );
            let waypoints = [];
            for (let ind3 in waypoints_temp)
                waypoints.push({ location: waypoints_temp[ind3] });
            let destination = data_transformed[data_transformed.length - 1];

            let res = calculateRouteTuples(origin, waypoints, destination);
        }
    }, [trigger_api, window.google]);
    // },[rider_places,window.google])

    // let isLoaded=true;
    const { isLoaded } = useJsApiLoader({
        googleMapsApiKey: "AIzaSyC-BWemSByl9AoF7KNOzaFDL503NNrjB_g",
        libraries: ["places"],
    });

    const [ishighligted, setIshighligted] = useState(false);
    const [map, setMap] = useState(/** @type google.maps.Map */ (null));
    const [directionsResponse, setDirectionsResponse] = useState(null);
    const [distance, setDistance] = useState("");
    const [curlat, setCurlat] = useState("");
    const [curlong, setCurlong] = useState("");
    const [duration, setDuration] = useState("");

    const originRef = useRef();
    const destiantionRef = useRef();
    const thirdplaceRef = useRef();

    if (!isLoaded) {
        return (
            <div style={{ width: "100%", height: "100%" }}>Loading ... </div>
        );
    }

    async function calculateRouteTuples(org, wp, dest) {
        const directionsService = new window.google.maps.DirectionsService();
        const results = await directionsService
            .route({
                origin: org,
                // waypoints : wp.slice(0,13),
                waypoints: wp,
                destination: dest,
                // eslint-disable-next-line no-undef
                travelMode: google.maps.TravelMode.DRIVING,
            })
            .then((results) => {
                setRenderitem((renderitem) => [...renderitem, results]);
                let totdist = 0;
                let tottime = 0;
                for (let i = 0; i < results.routes[0].legs.length; i++) {
                    let item = results.routes[0].legs[i];
                    totdist += item.distance.value;
                    tottime += item.duration.value;
                }
                totdist = (totdist / 1000).toFixed(2);
                tottime = (tottime / 60).toFixed(2);
                setStats((old) => [
                    ...old,
                    { distance: totdist, time: tottime },
                ]);

                //metrics
                setMin_time_state((old) => Math.min(old, tottime));
                setMax_time_state((old) => Math.max(old, tottime));
                setSum_time_state((old) =>
                    Math.round(Number(old) + Number(tottime))
                );

                setMin_dist_state((old) => Math.min(old, totdist));
                setMax_dist_state((old) => Math.max(old, totdist));
                setSum_dist_state((old) =>
                    Math.round(Number(old) + Number(totdist))
                );

                // console.log(results.routes);
            })
            .catch((err) => {
                console.log("error", err);
                // console.log(org);
                // console.log(wp);
                // console.log(dest);
            });

        // setDistance(results.routes[0].legs[0].distance.text)
        // setDuration(results.routes[0].legs[0].duration.text)
    }

    let handleClickHighLight = (key) => {
        let total_len = rider_places.length;
        if (setIshighligted == true || key == -1) {
            let arr = Array(total_len).fill(true);
            setShowRiderRoute((x) => arr);
        } else {
            let arr = Array(total_len).fill(false);
            arr[key] = true;
            setShowRiderRoute((x) => arr);
        }
        setIshighligted((x) => !x);
    };

    let handlePickUpSheet = () => {};

    return (
        <>
            {open ? (
                <Alert onClose={() => setOpen(false)}>Maps Updated</Alert>
            ) : null}

            <div className="jerry_directions2_contianer_top">
                <div className="jerry_directions2_map_container">
                    {/* start comment here */}
                    <GoogleMap
                        center={center}
                        zoom={15}
                        mapContainerStyle={{ width: "100%", height: "100%" }}
                        options={{
                            zoomControl: false,
                            streetViewControl: false,
                            mapTypeControl: false,
                            fullscreenControl: false,
                        }}
                        onLoad={(map) => setMap(map)}
                    >
                        {renderitem.map((data, index) => {
                            return (
                                <div>
                                    {showRiderRoute[index] && (
                                        <DirectionsRenderer
                                            key={index}
                                            directions={data}
                                            options={{
                                                polylineOptions: {
                                                    strokeColor: colors[index],
                                                },
                                            }}
                                        />
                                    )}
                                </div>
                            );
                        })}
                        {/* /> */}
                        {gotCenter ? (
                            <Marker
                                position={{
                                    lat: gotCenterData[0],
                                    lng: gotCenterData[1],
                                }}
                                icon={{
                                    path: "M 0,0 C -2,-20 -10,-22 -10,-30 A 10,10 0 1,1 10,-30 C 10,-22 2,-20 0,0 z",
                                    fillColor: "#0D25B2",
                                    fillOpacity: 0.8,
                                    strokeColor: "#FFFFFF",
                                    strokeWeight: 1,
                                }}
                            />
                        ) : null}
                    </GoogleMap>
                    {/* end comment here */}
                </div>

                <div className="jerry_directions2_rider_info">
                    <div className="jerry_routes_stats">
                        <div> Minimum Distance : {min_dist_state}</div>
                        <div> Maximum Distance: {max_dist_state}</div>
                        <div> Minimum Time : {min_time_state}</div>
                        <div> Maximum Time: {max_time_state}</div>
                        <div>
                            {" "}
                            Average Time:{" "}
                            {Math.round((sum_time_state / stats.length) * 100) /
                                100}
                        </div>
                        <div>
                            {" "}
                            Average Dist:{" "}
                            {Math.round((sum_dist_state / stats.length) * 100) /
                                100}{" "}
                        </div>
                        <div> Total Riders: {stats.length}</div>
                        <div className="jerry_routes_stats_bottom">
                            <button
                                className="jj_stats_button"
                                style={{ margin: "15px 0" }}
                                onClick={() => handleClickHighLight(-1)}
                            >
                                See All
                            </button>
                            <button
                                className="jj_stats_button"
                                style={{ margin: "15px 0" }}
                                // onClick={() => handlePickUpSheet()}
                                onClick={() => setShowUpload((x) => !x)}
                            >
                                {" "}
                                Pick Up Sheet{" "}
                            </button>
                        </div>
                    </div>
                    <div className="jerry_routes_bottom">
                        {stats.map((data, index) => (
                            <RiderCard
                                name={`rk${index + 1}@gmail.com`}
                                key={index}
                                index={index}
                                onClick_fn={handleClickHighLight}
                                color={colors[index]}
                                distance={data.distance}
                                time={data.time}
                            />
                        ))}
                    </div>
                </div>
            </div>

            {showUpload ? (
                <UploadExcel_Pickup
                    randomNumber={randomNumber}
                    setShowUpload={setShowUpload}
                    uploadedExcel={uploadedExcel}
                    setUploadedExcel={setUploadedExcel}
                    setRandomNumber={setRandomNumber}
                    token={token}
                    starter_fn={starter_fn}
                    triggerUseEffect={triggerUseEffect}
                    setTriggerUseEffect={setTriggerUseEffect}
                />
            ) : null}
        </>
    );
}

export default Directions2;
