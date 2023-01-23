import React, { useState, useEffect, useRef } from 'react'
import "./RiderCard.css"

function RiderCard({color, index, onClick_fn}) {

  const value2= useRef(1);
  
  useEffect(()=>{
    value2.current= index;
  },[])

  return (
    // <div className='jerry_ridercard_container' style={{backgroundColor:color}}  onClick={() => onClick_fn(value1)}>
    <div className='jerry_ridercard_container' style={{backgroundColor:color}}  onClick={() => onClick_fn(value2.current)}>
        <div>Name</div>
        <div>Distance</div>
        <div>Time</div>
    </div>
  )
}

export default RiderCard