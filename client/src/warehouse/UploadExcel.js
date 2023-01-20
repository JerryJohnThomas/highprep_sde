import React, { useEffect } from 'react'
import "./UploadExcel.css"


function UploadExcel({setShowUpload,token, islogged}) {
  
  let handleClick = (e) =>{
    console.log(e.target.className);
    if(e.target.className=="jj_uploadexcel_wrapper")
        setShowUpload(false);
  }

    return (
    <div className='jj_uploadexcel_wrapper' onClick={(e)=>handleClick(e)}>
        <div className='jj_uploadexcel_container'>
            UploadExcel

            // TO DO @shub
            have options for 
            * uploading an excel sheet
            * previewing the name 
            * maybe upload animation for v2
            * after upload response back do setSHowUpload(false) 
        </div>
    </div>
  )
}

export default UploadExcel