import React, { useEffect, useState } from "react";
import ExcelUploader from "./ExcelUploader";
import "./UploadExcel.css";
import axios from "../axios"
function UploadExcel_Pickup({ randomNumber, setShowUpload,starter_fn, token, islogged, uploadedExcel, setUploadedExcel, setRandomNumber,setRiders ,riders, triggerUseEffect, setTriggerUseEffect}) {

    let handleClick = (e) => {
        if (e.target.className == "jj_uploadexcel_wrapper")
            setShowUpload(false);
        console.log(token);
        console.log(randomNumber);
    };

    let handle_Submission = () => {
        //TO DO
        if (uploadedExcel == null) 
        {
            alert("Please choose an excel sheet");
            return;
        }
        
            console.log("token is ", token);
            console.log("randomNumber is ", randomNumber);
            const formData = new FormData();
            formData.append('file', uploadedExcel);
            formData.append('token', token);
            formData.append('randomNumber', randomNumber);
            // send both the files
            axios.post('/algo/dynamicpickup/', formData)
            .then((res) => { 
                // Handle response
                console.log("Successfully sent file");                
                setShowUpload(false);
                console.log("res");
                // setRandomNumber(res.data.randomNumber);
                setTriggerUseEffect((x) => x + 1);
                starter_fn();
                console.log("starter function tried to start");
            })
            .catch((err) => {
                // Handle error
                console.log(err)
                // alert("Try again");
            })
            
    };

    return (
        <div className="jj_uploadexcel_wrapper" onClick={(e) => handleClick(e)}>
            <div className="jj_uploadexcel_container">
                {/* UploadExcel

            // TO DO @shub
            have options for 
            * uploading an excel sheet
            * previewing the name 
            * maybe upload animation for v2
            * after upload response back do setSHowUpload(false)  */}

                <div className="jj_ue_upload_container">
                    <div className="jj_ue_left_no_border">
                        <div> Upload Excel Sheet </div>
                        <ExcelUploader
                            uploadedExcel={uploadedExcel}
                            setUploadedExcel={setUploadedExcel}
                        />
                    </div>
                    {/* <div className="jj_ue_right">
                        <div>Enter number of riders </div>
                        <input
                            type="number"
                            className="input_field1"
                            defaultValue="5"
                            value={riders}
                            onChange={(e) => {
                                setRiders(e.target.value);
                            }}
                        ></input>
                    </div> */}
                </div>
                <div className="jj_ue_btn_container">
                    <button
                        className="jj_stats_button"
                        onClick={() => handle_Submission()}
                    >
                        Submit
                    </button>
                </div>
            </div>
        </div>
    );
}

export default UploadExcel_Pickup;
