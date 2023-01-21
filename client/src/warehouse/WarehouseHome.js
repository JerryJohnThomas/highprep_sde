import React, { useEffect } from 'react'
import { useState } from 'react'
import UploadExcel from './UploadExcel'
import "./WarehouseHome.css"


function WarehouseHome({token, islogged}) {


  const[places, setPlaces]= useState(32)
  const[riders, setRiders]= useState(0)
  const[showUpload, setShowUpload] = useState(false)


  useEffect(()=>{
    updateStats()
  },[showUpload])

  let updateStats = () =>{
    //call backend and get the number of points and number of riders 
    // and set the     
    // TO DO @rupesh jerry

  }

  let startAlgo = () =>{
    if(places == 0 || riders == 0)
    {
      alert("places or riders are 0, kindly make it non zero before running")
      return;
    }

    // start calling get function tell we get a response 


    // if we get a response make the page shift to maps and that will do the rest 



    
  }

  let sampleAlgo = ()=>{

  }

  return (
    <div>
      <div className='jj_stats_wrapper'>
        <div className="jj_stats_container">
          <div className="jj_stats_left jj_stats_item"><div>{places}</div><div>places</div></div>
          <div className="jj_stats_middle jj_stats_item"><div>{riders}</div><div>riders</div></div>
          <div className="jj_stats_right jj_stats_item">

            <button className='jj_stats_button' onClick={()=>setShowUpload(x=>!x)}>Upload New Excel</button>
            <button className='jj_stats_button' onClick={()=>startAlgo()}>Start Analysing</button>
            <button className='jj_stats_button' onClick={()=>sampleAlgo()}>Use Sample Dataset</button>


          </div>
        </div>
        {showUpload?<UploadExcel setShowUpload={setShowUpload} />:null}
      </div>
      {/* <div>
        options
        <div>start algo </div>
        <div>use sample dataset</div>
      </div> */}
      
      </div>



  )
}

export default WarehouseHome