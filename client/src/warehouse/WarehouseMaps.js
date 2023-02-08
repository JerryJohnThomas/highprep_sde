import React, { useEffect } from 'react'
import Directions2 from './Directions2'


function WarehouseMaps({setRandomNumber,randomNumber, token, islogged}) {
  useEffect(()=>{
    console.log("got inputs as");
    console.log("random: ");
    console.log(randomNumber);
    console.log("token: ");
    console.log(token);
  },[])

  
  return (
    <>
      {/* <div>Warehouse    Maps</div> */}
      {/* <Directions2 randomNumber={"gutatlpv1o"} token={"33fc7ab5df252f5e197d8fbdb7f28a7d06421a5f"} islogged={islogged} /> */}
      <Directions2 setRandomNumber={setRandomNumber} randomNumber={randomNumber} token={token} islogged={islogged} />
    </>
    
  )
}

export default WarehouseMaps