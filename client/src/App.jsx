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
import RiderMap from "./rider/RiderMap";
import GoogleMapsDirections from "./rider/GoogleMapsDirections";

import RiderBag from "./rider/riderBag.jsx";
import Delivery from "./rider/delivery";
import Camera from "./Camera";
import Camera2 from "./camera2";
import InputIt from "./common/InputIt";
function App() {
    const [islogged, setIsLogged] = useState(false);
    // const[islogged, setIsLogged] = useState(true)
    const [token, setToken] = useState(
        "33fc7ab5df252f5e197d8fbdb7f28a7d06421a5f"
    );
    const [query, setQueryState] = useState("rk5@gmail.com");
    const [randomNumber, setRandomNumber] = useState(
        // "ka509l1tul"
        // "epb88up2ek"
        "zy2h00iubx"
    );

    return (
        <div>
            <Router>
                <Navbar islogged={islogged} setIsLogged={setIsLogged} />
                <Routes>
                    <Route
                        exact
                        path="/warehouse/"
                        element={
                            <WarehouseHome
                                randomNumber={randomNumber}
                                setRandomNumber={setRandomNumber}
                                token={token}
                                islogged={islogged}
                            />
                        }
                    />

                    <Route
                        exact
                        path="/warehouse/items"
                        element={
                            <DataTable token={token} islogged={islogged} />
                        }
                    />
                    <Route
                        exact
                        path="/warehouse/home"
                        element={
                            <WarehouseHome
                                randomNumber={randomNumber}
                                setRandomNumber={setRandomNumber}
                                token={token}
                                islogged={islogged}
                            />
                        }
                    />

                    <Route
                        exact
                        path="/warehouse/upload"
                        element={
                            <UploadExcel token={token} islogged={islogged} />
                        }
                    />

                    <Route
                        exact
                        path="/warehouse/inventory"
                        element={
                            <WarehouseInventory
                                token={token}
                                islogged={islogged}
                            />
                        }
                    />
                    <Route
                        exact
                        path="/warehouse/maps"
                        element={
                            <WarehouseMaps
                                randomNumber={randomNumber}
                                setRandomNumber={setRandomNumber}
                                token={token}
                                islogged={islogged}
                            />
                        }
                    />
                    <Route
                        exact
                        path="/customer/home"
                        element={
                            <CustomerHome token={token} islogged={islogged} />
                        }
                    />

                    <Route exact path="/cam" element={<Camera />} />
                    <Route exact path="/cam2" element={<Camera2 />} />
                    <Route
                        exact
                        path="/rider/home"
                        element={
                            <RiderHome token={token} islogged={islogged} />
                        }
                    />
                    <Route exact path="/rider/bag" element={<RiderBag />} />
                    <Route
                        exact
                        path="/rider/delivery"
                        element={<Delivery />}
                    />

                    <Route
                        exact
                        path="/rider/maps"
                        element={
                            <GoogleMapsDirections
                                token={token}
                                islogged={islogged}
                                randomNumber={randomNumber}
                                email={query}
                            />
                        }
                    />
                    <Route
                        exact
                        path="/home"
                        element={<Home token={token} islogged={islogged} />}
                    />

                    <Route
                        exact
                        path="/config"
                        element={
                            <InputIt
                                token={token}
                                setToken={setToken}
                                randomNumber={randomNumber}
                                setRandomNumber={setRandomNumber}
                            />
                        }
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
                                query={query}
                                setQueryState={setQueryState}
                            />
                        }
                    />
                </Routes>
            </Router>
        </div>
    );
}

export default App;
