import Home from "./Home";
import Demo from "./customer/demo";
import DataTable from "./warehouse/itemInv";
import "./App.css";
import {
  BrowserRouter as Router,
  // Switch,
  Route,
  Redirect,
} from "react-router-dom";

import { Routes } from "react-router-dom";
import WarehouseHome from "./warehouse/WarehouseHome";
import WarehouseInventory from "./warehouse/WarehouseInventory";
import WarehouseMaps from "./warehouse/WarehouseMaps";
import CustomerHome from "./customer/CustomerHome";
import RiderHome from "./rider/RiderHome";
import Login from "./login/login";
import Navbar from "./common/Navbar";
import { useState } from "react";
import UploadExcel from "./warehouse/UploadExcel";
<<<<<<< HEAD
import Delivery from "./rider/delivery";

function App() {
  // const[islogged, setIsLogged] = useState(false)
  const [islogged, setIsLogged] = useState(true);
  const [token, setToken] = useState("");
=======
import RiderMap from "./rider/RiderMap";


function App() {
    const[islogged, setIsLogged] = useState(false)
    // const[islogged, setIsLogged] = useState(true)
    const [token, setToken] = useState("");
>>>>>>> 590704a585fc380f2ee6a4cb8f43364a16304ff2

  return (
    <div>
      <Router>
        <Navbar islogged={islogged} setIsLogged={setIsLogged} />
        <Routes>
          <Route
            exact
            path="/warehouse/"
            element={<WarehouseHome token={token} islogged={islogged} />}
          />

          <Route
            exact
            path="/warehouse/items"
            element={<DataTable token={token} islogged={islogged} />}
          />
          <Route
            exact
            path="/warehouse/home"
            element={<WarehouseHome token={token} islogged={islogged} />}
          />

          <Route
            exact
            path="/warehouse/upload"
            element={<UploadExcel token={token} islogged={islogged} />}
          />

          <Route
            exact
            path="/warehouse/inventory"
            element={<WarehouseInventory token={token} islogged={islogged} />}
          />
          <Route
            exact
            path="/warehouse/maps"
            element={<WarehouseMaps token={token} islogged={islogged} />}
          />
          <Route
            exact
            path="/customer/home"
            element={<CustomerHome token={token} islogged={islogged} />}
          />

<<<<<<< HEAD
          <Route
            exact
            path="/rider/home"
            element={<RiderHome token={token} islogged={islogged} />}
          />
          <Route
            exact
            path="/home"
            element={<Home token={token} islogged={islogged} />}
          />
          <Route
            exact
            path="/"
            element={<Home token={token} islogged={islogged} />}
          />
          <Route
            exact
            path="/login"
            element={
              <Login
                islogged={islogged}
                setIsLogged={setIsLogged}
                token={token}
                setToken={setToken}
              />
            }
          />
          <Route exact path="/rider/delivery" element={Delivery} />
        </Routes>
      </Router>
    </div>
  );
=======
                    <Route
                        exact
                        path="/rider/home"
                        element={
                            <RiderHome token={token} islogged={islogged} />
                        }
                    />


                     <Route
                        exact
                        path="/rider/maps"
                        element={
                            <RiderMap token={token} islogged={islogged} />
                        }
                    />
                    <Route
                        exact
                        path="/home"
                        element={<Home token={token} islogged={islogged} />}
                    />
                    <Route
                        exact
                        path="/"
                        element={<Home token={token} islogged={islogged} />}
                    />
                    <Route
                        exact
                        path="/login"
                        element={
                            <Login
                                islogged={islogged}
                                setIsLogged={setIsLogged}
                                token={token}
                                setToken={setToken}
                            />
                        }
                    />
                </Routes>
            </Router>
        </div>
    );
>>>>>>> 590704a585fc380f2ee6a4cb8f43364a16304ff2
}

export default App;
