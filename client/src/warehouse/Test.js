import React, { useEffect, useState } from 'react'

function Test() {
    
    const[a,b]=useState([[0,1],[2,3]])
    useEffect(()=>{
        b((old)=>[...old, "test"])
        console.log(a)
    },[])
    



  return (
    <div>Test</div>
  )
}

export default Test