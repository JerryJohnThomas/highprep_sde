import React from 'react'
import "./RiderCard.css"

function RiderCard({color}) {
  return (
    <div className='jerry_ridercard_container' style={{backgroundColor:color}}>
        <div>Name</div>
        <div>Distance</div>
        <div>Time</div>
    </div>
  )
}

export default RiderCard