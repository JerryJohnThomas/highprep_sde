import React, { useState, useEffect } from "react";
import {
    GoogleMap,
    DirectionsRenderer,
    LoadScript,
} from "@react-google-maps/api";
import "./GoogleMapsDirections.css";

import TurnRightIcon from "@mui/icons-material/TurnRight";
import TurnLeftIcon from "@mui/icons-material/TurnLeft";
import StraightIcon from "@mui/icons-material/Straight";
import UTurnRightIcon from "@mui/icons-material/UTurnRight";

const GoogleMapsDirections = () => {
    const [directions, setDirections] = useState(null);

    useEffect(() => {
        // window.google.addEventListener('load', () => {
        //   console.log("suprise");
        // });

        if (!window.google) {
            console.log("window google not loaded");
            the_magic_do_it_all_function();
        } else {
            console.log("window google loaded");
            the_magic_do_it_all_function();
        }
    }, [window.google]);

    // let the_magic_do_it_all_function = () =>{
    async function the_magic_do_it_all_function() {
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
                    destination: end,
                    travelMode: window.google.maps.TravelMode.DRIVING,
                },
                (result, status) => {
                    console.log("res");
                    if (status === window.google.maps.DirectionsStatus.OK) {
                        console.log(result);
                        console.log(result.length);
                        console.log(result.routes[0].legs[0].steps);
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
                {directions ? (
                    directions.routes[0].legs[0].steps.map((data, index) => (
                        <DirectionCard data={data} index={index} />
                    ))
                ) : (
                    <div
                        style={{
                            height: "90%",
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
                                {" "}
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
export default GoogleMapsDirections;

// https://developers.google.com/maps/documentation/routes_preferred/reference/rest/Shared.Types/Maneuver#:~:text=Stay%20organized%20with%20collections%20Save%20and%20categorize%20content%20based%20on%20your%20preferences.&text=A%20set%20of%20values%20that,%2C%20straight%2C%20etc.).
