import React, { useEffect } from 'react'
import { useState } from 'react'
import UploadExcel from './UploadExcel'
import "./WarehouseHome.css"
import axios from "../axios"
// import axios from "axios";
import { useNavigate } from "react-router-dom";

function WarehouseHome({token, islogged}) {
    const navigate = useNavigate();


  const[places, setPlaces]= useState(32)
  const[riders, setRiders]= useState(6)
  const[showUpload, setShowUpload] = useState(false)
  const [uploadedExcel, setUploadedExcel] = useState(null);
  const [randomNumber, setRandomNumber] = useState(null);

  

  useEffect(()=>{
    updateStats()
  },[showUpload])

  let updateStats = () =>{
    //call backend and get the number of points and number of riders 
    // and set the     
    // TO DO @rupesh jerry

    

  }

  let startAlgo = () =>{
    // if(places == 0 || riders == 0)
    // {
    //   alert("places or riders are 0, kindly make it non zero before running")
    //   return;
    // }

fetchData()
    // start calling get function tell we get a response 


    // if we get a response make the page shift to maps and that will do the rest 



    
  }



    async function fetchData() {
      const response = await axios.get(
        // 'https://8f1f-2409-4073-4d8e-70c9-3091-6b34-1a8f-f73c.in.ngrok.io/algo/status/',
        '/algo/status/',
               {
              token: "4a14c34983a572b87fce0255ec2a6c7ec5a52a91",
              randomNumber : "lfe8m4uxkh"
            }
            ).then((data)=>{

              console.log(data);
              console.log(data.data);
            }
            ).catch((err) =>
            console.log(err));

    }

  let sampleAlgo = ()=>{


    // .get(`/algo/start/`)
    axios
        .post(`/algo/status/`, 
            {
              "token": "4a14c34983a572b87fce0255ec2a6c7ec5a52a91",
              "randomNumber" : "lfe8m4uxkh"
            }
        )
        .then((res) => {
            console.log(res.data);
            navigate("/warehouse/maps", { replace: true });

            // setFormState("DONE");
            // setResultState(res.data);
        })
        .catch((error) => {
            // setFormState("ERROR");
            console.log(error);
        });

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
        {showUpload?<UploadExcel 
                                  setShowUpload={setShowUpload}
                                  uploadedExcel={uploadedExcel}
                                  setUploadedExcel={setUploadedExcel}
                                  setRandomNumber={setRandomNumber}
                                   />:null}
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