import React, { useEffect, useState } from "react";
import ExcelUploader from "./ExcelUploader";
import "./UploadExcel.css";

function UploadExcel({ setShowUpload, token, islogged }) {
    const [riders, setRiders] = useState(5);
    const [uploadedExcel, setUploadedExcel] = useState(null);

    let handleClick = (e) => {
        console.log(e.target.className);
        if (e.target.className == "jj_uploadexcel_wrapper")
            setShowUpload(false);
    };

    let handle_Submission = () => {
        //TO DO
        if (uploadedExcel == null) alert("Please choose an excel sheet");
        // send both the files
        


      setShowUpload(false);
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
                    <div className="jj_ue_left">
                        <div> Upload Excel Sheet </div>
                        <ExcelUploader
                            uploadedExcel={uploadedExcel}
                            setUploadedExcel={setUploadedExcel}
                        />
                    </div>
                    <div className="jj_ue_right">
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
                    </div>
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

export default UploadExcel;
