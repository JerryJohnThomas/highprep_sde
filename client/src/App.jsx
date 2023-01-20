import Home from "./Home";
import Demo from "./customer/demo";
import DataTable from "./warehouse/itemInv";
import "./App.css"
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
function App() {
    return (
        <div>
            <Router>
                <Routes>
                    <Route
                        exact
                        path="/warehouse/itemInv"
                        element={<DataTable />}
                    />
                    <Route
                        exact
                        path="/warehouse/home"
                        element={<WarehouseHome />}
                    />
                    <Route
                        exact
                        path="/warehouse/inventory"
                        element={<WarehouseInventory />}
                    />
                    <Route
                        exact
                        path="/warehouse/maps"
                        element={<WarehouseMaps />}
                    />
                    <Route
                        exact
                        path="/customer/home"
                        element={<CustomerHome />}
                    />

                    <Route exact path="/rider/home" element={<RiderHome />} />
                    <Route exact path="/home" element={<Home />} />
                    <Route exact path="/" element={<Home />} />
                    <Route exact path="/login" element={<Login />} />
                </Routes>
            </Router>
        </div>
    );
}

export default App;
