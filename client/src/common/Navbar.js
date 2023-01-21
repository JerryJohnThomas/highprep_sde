import React from 'react'
import Log from './Log'
import "./Navbar.css"

function Navbar({islogged,setIsLogged}) {
  return (
    <div className="jerry_navbar_container">
        <div className='jj_navbar_left'>RouteIt</div>
        <div className='jj_navbar_right'><Log islogged={islogged} setIsLogged={setIsLogged} /></div>
    </div>
  )
}
export default Navbar