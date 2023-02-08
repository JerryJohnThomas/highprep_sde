import React, { useState } from 'react'

function InputIt({token,setToken, randomNumber, setRandomNumber}) {
  
    const[token_inp,setToken_inp] = useState("");
    const[rand_inp,setRand_inp] = useState("");
    
    let handle =()=>{
        console.log("token", token)
        console.log("randomNumber", randomNumber)
    }
    return (
    <>
    <div style={{margin:"20px"}}>
        <div>Token Value</div>
    <input value={token_inp}  onChange={(e)=> setToken_inp(e.target.value)}  type="text"></input>
    <button  className="jj_stats_button" onClick={(e)=>setToken(token_inp)}> Set </button>  
        <br></br>
        <br></br>
        <br></br>
    <div>Random value</div>
    <input value={rand_inp} onChange={(e)=> setRand_inp(e.target.value)}  type="text"></input>
    <button className="jj_stats_button" onClick={(e)=>setRandomNumber(token_inp)}>Set</button>  
    </div>


    <button onClick={(e)=>handle()}>tnx</button>
    </>


  )
}

export default InputIt