import React, { useEffect } from "react";
import { useState } from "react";
import UploadExcel from "./UploadExcel";
import "./WarehouseHome.css";
import axios from "../axios";
// import axios from "axios";
import { useNavigate, Link } from "react-router-dom";

function WarehouseHome({ randomNumber, setRandomNumber, token, islogged }) {
    const navigate = useNavigate();

    const [places, setPlaces] = useState(32);
    const [riders, setRiders] = useState(5);
    const [showUpload, setShowUpload] = useState(false);
    const [uploadedExcel, setUploadedExcel] = useState(null);

    useEffect(() => {
        updateStats();
    }, [showUpload]);

    let updateStats = () => {
        //call backend and get the number of points and number of riders
        // and set the
        // TO DO @rupesh jerry
    };

    let startAlgo = () => {
        console.log(randomNumber);
        // if(places == 0 || riders == 0)
        // {
        //   alert("places or riders are 0, kindly make it non zero before running")
        //   return;
        // }

        /*

      algo/start/
          token:
          randomNumner:



      algo/status/
        token:
        randomNumner:

        res.msg = "Algorithm Finished"
          if complete

          else
            "Algo is still going on"
        


    */

        // uncomment this
        StartAlgo_fn();
        // start calling get function tell we get a response
        // if we get a response make the page shift to maps and that will do the rest
    };

    async function StartAlgo_fn() {
        console.log("token", token);
        console.log("randomNumber", randomNumber);
        let temp = false;
        const response = await axios
            .post(
                // 'https://8f1f-2409-4073-4d8e-70c9-3091-6b34-1a8f-f73c.in.ngrok.io/algo/status/',
                "/algo/start/",
                {
                    token: token,
                    randomNumber: randomNumber,
                    n: riders,
                }
            )
            .then((data) => {
                console.log(data);
                console.log(data.data);
                temp = true;
            })
            .catch((err) => console.log(err));
        console.log("temp", temp);
        runUntilTrue();
    }

    const runUntilTrue = async () => {
        let result = false;
        console.log("runUntilTrue");
        while (!result) {
            await new Promise((resolve) =>
                setTimeout(() => {
                    result = isOver();
                    console.log(result);
                    if(result)
                        navigate("/warehouse/maps");
                    resolve(result);
                    console.log(result);
                }, 1000 * 15)
            );
        }
    };

    async function isOver() {
        console.log("token", token);
        console.log("randomNumber", randomNumber);
        const response = await axios
            .post(
                // 'https://8f1f-2409-4073-4d8e-70c9-3091-6b34-1a8f-f73c.in.ngrok.io/algo/status/',
                "/algo/status/",
                {
                    token: token,
                    randomNumber: randomNumber,
                }
            )
            .then((data) => {
                console.log(data.data.msg);
                if (data.data.msg == "Algorithm Finished") return true;
                else return false;
            })
            .catch((err) => {
                console.log(err);
                return false;
            });

        return false;
    }
    let sampleAlgo = () => {
        navigate("/warehouse/maps");

        // navigate("/warehouse/maps", { randomNumber:"gutatlpv1o", token: "33fc7ab5df252f5e197d8fbdb7f28a7d06421a5f",  replace: true });
        // navigate("/warehouse/maps", state={{token: 12 ,randomNumber:"gutatlpv1o"}})

        // axios
        //     .post(`/algo/status/`,
        //         {
        //           "token": {token},
        //           "randomNumber" : "lfe8m4uxkh"
        //         }
        //     )
        //     .then((res) => {
        //         console.log(res.data);
        //         navigate("/warehouse/maps", { replace: true });

        //         // setFormState("DONE");
        //         // setResultState(res.data);
        //     })
        //     .catch((error) => {
        //         // setFormState("ERROR");
        //         console.log(error);
        //     });
    };

    return (
        <div>
            <div className="jj_stats_wrapper">
                <div className="jj_stats_container">
                    <div className="jj_stats_left jj_stats_item">
                        <div>{places}</div>
                        <div>places</div>
                    </div>
                    <div className="jj_stats_middle jj_stats_item">
                        <div>{riders}</div>
                        <div>riders</div>
                    </div>
                    <div className="jj_stats_right jj_stats_item">
                        <button
                            className="jj_stats_button"
                            onClick={() => setShowUpload((x) => !x)}
                        >
                            Upload New Excel
                        </button>
                        <button
                            className="jj_stats_button"
                            onClick={() => startAlgo()}
                        >
                            Start Analysing
                        </button>
                        <button
                            className="jj_stats_button"
                            onClick={() => sampleAlgo()}
                        >
                            Use Sample Dataset
                        </button>
                        {/* <Link to="/warehouse/maps" state={{  token: "value", randomNumber : "asd" }} >ok</Link> */}
                    </div>
                </div>
                {showUpload ? (
                    <UploadExcel
                        setShowUpload={setShowUpload}
                        uploadedExcel={uploadedExcel}
                        setUploadedExcel={setUploadedExcel}
                        setRandomNumber={setRandomNumber}
                        token={token}
                        setRiders={setRiders}
                        riders={riders}
                    />
                ) : null}
            </div>
            {/* <div>
        options
        <div>start algo </div>
        <div>use sample dataset</div>
      </div> */}
        </div>
    );
}

export default WarehouseHome;
