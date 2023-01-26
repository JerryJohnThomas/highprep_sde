import React, { useState, useEffect, useRef } from 'react'
import "./RiderCard.css"

function RiderCard({color, name, index, onClick_fn, distance, time}) {

  const value2= useRef(1);
  
  useEffect(()=>{
    value2.current= index;
  },[])

  return (
    // <div className='jerry_ridercard_container' style={{backgroundColor:color}}  onClick={() => onClick_fn(value1)}>
    <div className='jerry_ridercard_container' style={{backgroundColor:color}}  onClick={() => onClick_fn(value2.current)}>
        <div>Name: {} </div>
        <div>Distance: {distance} km</div>
        <div>Time: {time} min</div>
    </div>
  )
}

export default RiderCard