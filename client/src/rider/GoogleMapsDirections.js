import React, { useState, useEffect } from "react";
import {
    GoogleMap,
    DirectionsRenderer,
    LoadScript,
    Data,
} from "@react-google-maps/api";
import "./GoogleMapsDirections.css";

import TurnRightIcon from "@mui/icons-material/TurnRight";
import TurnLeftIcon from "@mui/icons-material/TurnLeft";
import StraightIcon from "@mui/icons-material/Straight";
import UTurnRightIcon from "@mui/icons-material/UTurnRight";
import axios from "../axios";
import Map_inside from "./Map_inside";

const GoogleMapsDirections = ({ token, islogged, randomNumber }) => {
    const [directions, setDirections] = useState(null);
    const [locdata, setLocdata] = useState(null);
    const [rider_places, setRiderplaces] = useState([]);
    const [trigger_api, setTrigger_api] = useState(1);
    const [sum_time_state, setSum_time_state] = useState(0);
    const [sum_dist_state, setSum_dist_state] = useState(0);
    useEffect(() => {
        // getLocations();
        sequentialExecution();
    }, []);

    const sequentialExecution = async () => {
        try {
            const data1 = await getLocations();
            const data2 = await convertTOgooglePoints();
            return data2;
        } catch (error) {
            console.error(error);
        }
    };

    const getLocations = async () => {
        axios
            .post(`/algo/status/`, {
                token: token,
                randomNumber: randomNumber,
            })
            .then((res) => {
                setRiderplaces([]);
                let data = res.data;
                let rider_to_loc = data.rider_to_location;
                for (let i = 0; i < rider_to_loc.length; i++) {
                    let temp = [];
                    let rid = { rider_id: rider_to_loc[i].email };
                    if (rider_to_loc[i].email != "rk4@gmail.com") continue;
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
                    console.log(" getLocations over");
                }
            })
            .catch((error) => {
                console.log(error);
            })
            .finally(() => setTrigger_api((x) => x + 1));
    };

    useEffect(() => {
        convertTOgooglePoints();
    }, [trigger_api]);

    const convertTOgooglePoints = () => {
        console.log("started convertTOgooglePoints ", rider_places.length);
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
            console.log(" convert to google points over", origin);

            let res = the_magic_do_it_all_function(
                origin,
                waypoints,
                destination
            );
        }
    };

    // useEffect(() => {
    //     // window.google.addEventListener('load', () => {
    //     //   console.log("suprise");
    //     // });

    //     if (!window.google) {
    //         console.log("window google not loaded");
    //         the_magic_do_it_all_function();
    //     } else {
    //         console.log("window google loaded");
    //         the_magic_do_it_all_function();
    //     }
    // }, [window.google]);

    // let the_magic_do_it_all_function = () =>{
    async function the_magic_do_it_all_function(
        origin,
        waypoints,
        destination
    ) {
        console.log("Started magic function");
        const directionsService = new window.google.maps.DirectionsService();
        navigator.geolocation.getCurrentPosition((position) => {
            const start = {
                lat: position.coords.latitude,
                lng: position.coords.longitude,
            };
            const end = {
                lat: 10.015,
                lng: 76.34,
            };

            directionsService.route(
                {
                    origin: start,
                    waypoints: waypoints,
                    destination: destination,
                    travelMode: window.google.maps.TravelMode.DRIVING,
                },
                (result, status) => {
                    console.log("res");
                    if (status === window.google.maps.DirectionsStatus.OK) {
                        console.log(result);
                        console.log(result.length);
                        // console.log(result.routes[0].legs[0].steps);
                        setDirections(result);

                        //stats
                        let totdist = 0;
                        let tottime = 0;
                        for (let i = 0; i < result.routes[0].legs.length; i++) {
                            let item = result.routes[0].legs[i];
                            totdist += item.distance.value;
                            tottime += item.duration.value;
                        }
                        totdist = (totdist / 1000).toFixed(2);
                        tottime = (tottime / 60).toFixed(2);
                        // time in sec  and dist in meteres originally
                        // when converting we get in min and km

                        //metrics
                        setSum_time_state((old) =>
                            Math.round(Number(old) + Number(tottime))
                        );

                        setSum_dist_state((old) =>
                            Math.round(Number(old) + Number(totdist))
                        );
                    } else {
                        console.error(`error fetching directions ${result}`);
                    }
                }
            );
        });
    }

    let PickUpAction = () => {
        //axios code
    };

    //DeliveryAction

    let DeliveryAction = () => {
        //axios code
    };

    let RefreshAction = () => {
        sequentialExecution();
    };

    return (
        <div className="gmd_container">
            <div className="gmd_left">
                <LoadScript googleMapsApiKey="AIzaSyC-BWemSByl9AoF7KNOzaFDL503NNrjB_g">
                    <GoogleMap
                        mapContainerStyle={{
                            // height: "800px",
                            height: "100%",
                            width: "100%",
                        }}
                        center={{
                            lat: 10.85073,
                            lng: 76.65126,
                        }}
                        zoom={10}
                    >
                        {directions && (
                            <DirectionsRenderer directions={directions} />
                        )}
                    </GoogleMap>
                </LoadScript>
            </div>

            <div className="gmd_right">
                <div className="gmd_right_title">Route Info</div>
                <div className="jj_rider_maps_right_top">
                    <div className="gmd_right_title">
                        Total Distance : {sum_dist_state} km
                    </div>
                    <div className="gmd_right_title">
                        Total time : {sum_time_state / 60} min
                    </div>
                    <div className="jj_btn_rider_horizontal">
                        <button
                            className="jj_stats_button"
                            onClick={() => DeliveryAction()}
                        >
                            delivery
                        </button>
                        <button
                            className="jj_stats_button"
                            onClick={() => PickUpAction()}
                        >
                            {" "}
                            pickup
                        </button>

                        <button
                            className="jj_stats_button"
                            onClick={() => RefreshAction()}
                        >
                            refresh
                        </button>
                    </div>
                </div>

                {directions ? (
                    directions.routes[0].legs.map(
                        (data0, index0) => <Mapper_inside data0={data0} index0={index0} />
                        // <Map_inside data0={data0} />
                    )
                ) : (
                    <div
                        style={{
                            height: "70%",
                            display: "flex",
                            justifyContent: "center",
                            alignItems: "center",
                        }}
                    >
                        {/* <div className="gmd_right_title">Waiting for directions</div> */}
                        <div>
                            <button
                                className="jj_stats_button"
                                onClick={() => the_magic_do_it_all_function()}
                            >
                                Get Directions{" "}
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

const DirectionCard = ({ data, index }) => {
    return (
        <div className="DirectionCard_container">
            <div className="DirectionCard_left">
                <div>
                    Distance: {data.distance.text} Time : {data.duration.text}
                </div>
                <div dangerouslySetInnerHTML={{ __html: data.instructions }} />
            </div>
            <div className="DirectionCard_right">
                {(data.maneuver == "turn-slight-left" ||
                    data.maneuver == "turn-sharp-left" ||
                    data.maneuver == "turn-left" ||
                    data.maneuver == "ramp-left" ||
                    data.maneuver == "fork-left" ||
                    data.maneuver == "roundabout-left") && <TurnLeftIcon />}

                {(data.maneuver == "turn-slight-right" ||
                    data.maneuver == "turn-sharp-right" ||
                    data.maneuver == "turn-right" ||
                    data.maneuver == "ramp-right" ||
                    data.maneuver == "fork-right" ||
                    data.maneuver == "roundabout-right") && <TurnRightIcon />}

                {(data.maneuver == "straight" ||
                    data.maneuver == "" ||
                    data.maneuver == "keep-right" ||
                    data.maneuver == "keep-left") && <StraightIcon />}

                {(data.maneuver == "uturn-right" ||
                    data.maneuver == "uturn-left") && <UTurnRightIcon />}
            </div>
        </div>
    );
};

const Mapper_inside = ({ data0, index0 }) => {
    return (
        <>
            <div style={{ textAlign: "center", fontWeight:"bold", margin:"5px 0" }}>
                Location {String.fromCharCode(index0+65)} 
            </div>
            {data0.steps.map((data, index) => (
                <DirectionCard data={data} index={index} />
            ))}
        </>
    );
};
export default GoogleMapsDirections;

// https://developers.google.com/maps/documentation/routes_preferred/reference/rest/Shared.Types/Maneuver#:~:text=Stay%20organized%20with%20collections%20Save%20and%20categorize%20content%20based%20on%20your%20preferences.&text=A%20set%20of%20values%20that,%2C%20straight%2C%20etc.).
