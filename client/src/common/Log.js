import React from 'react'
import {
    BrowserRouter as Router,
    Link,
    useLocation
  } from "react-router-dom";
function Log({islogged,setIsLogged}) {
  return (
    <>
    {
      
      islogged?
      <div className="jj_log_text" onClick={() => setIsLogged(false)}>Log Out</div>:
          <Link to="/login">
              <div className="jj_log_text">Log In </div>
          </Link>

    }
    </>
  )
}

export default Log