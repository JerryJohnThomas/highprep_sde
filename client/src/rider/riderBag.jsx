import React, { useState, useEffect, useRef } from "react";

//import * as React from 'react';
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import { Button } from "@mui/material";
import Delivery from "./delivery";
import axios from "axios";
import "./riderBag.css";
import { useNavigate } from "react-router-dom";

function createData(id, deliver_to, item_weight) {
  return { id, deliver_to, item_weight };
}

const rows = [
  createData(1, 159, 6.0),
  createData(2, 159, 6.0),
  createData(3, 159, 6.0),
];

export default function RiderBag() {
  console.log("in");
  const navigate = useNavigate();
  const [formState, setFormState] = useState("FETCHING_DATA");
  const [result, setResultState] = useState("");
  const [delItem, setdelItemState] = useState();
  const [delTo, setdelToState] = useState();
  // useEffect(() => {

  //     let axiosConfig = {
  //         headers: {
  //             "Content-Type": "application/json;charset=UTF-8",
  //             "Access-Control-Allow-Origin": "*",
  //         },
  //     };

  //     let fetchData = async () => {
  //         try {
  //             const result = await axios.get(`/inventory/`, axiosConfig);
  //             console.log(result.data);
  //         } catch (err) {
  //             if (err.message === "Network Error") {
  //                 console.log("Error: net::ERR_FAILED with status code 200");
  //                 console.log(err);
  //             }
  //         }
  //     };
  //     fetchData();
  // }, []);
  const handleDelivery = (itemId, deliver_to) => {
    setdelItemState(itemId);
    setdelToState(deliver_to);
    setFormState("DELIVERING");
  };
  const attemptDelivery = () => {
    //attempt delivery
    setFormState("FETCHING_DATA");
  };
  useEffect(() => {
    if (formState === "FETCHING_DATA") {
      axios
        .get("https://mocki.io/v1/5fcbc89d-f2f2-4abe-abb7-596f295a6d24")
        .then((res) => {
          console.log(res.data);
          setFormState("DONE");
          setResultState(res.data);
        })
        .catch((error) => {
          setFormState("ERROR");
          console.log(error);
        });
    }
  }, [formState]);
  if (formState === "DELIVERING") {
    navigate("/rider/delivery", {
      state: { itemIdP: delItem, deliver_toP: delTo },
    });
    //return <Delivery itemIdP={delItem} deliver_toP={delTo} />;
  }
  if (formState === "DONE") {
    console.log("bro");
    return (
      <div className="layer1">
        {/* <h1>Inventory (change column names)</h1> */}
        <h1>Bag Inventory </h1>
        <div>
          <TableContainer component={Paper}>
            <Table sx={{ minWidth: 650 }} aria-label="simple table">
              <TableHead>
                <TableRow>
                  <TableCell>id (100g serving)</TableCell>
                  <TableCell align="right">Item Name</TableCell>
                  <TableCell align="right">Item Volume&nbsp;(g)</TableCell>
                  {/* <TableCell align="right">Carbs&nbsp;(g)</TableCell>
            <TableCell align="right">Protein&nbsp;(g)</TableCell> */}
                </TableRow>
              </TableHead>
              <TableBody>
                {rows.map((row) => (
                  <TableRow
                    key={row.id}
                    sx={{
                      "&:last-child td, &:last-child th": { border: 0 },
                    }}
                  >
                    <TableCell component="th" scope="row">
                      {row.id}
                    </TableCell>
                    <TableCell align="right">{row.deliver_to}</TableCell>
                    <TableCell align="right">{row.item_weight}</TableCell>
                    {/* <TableCell align="right">{row.carbs}</TableCell>
              <TableCell align="right">{row.protein}</TableCell> */}
                    <TableCell align="center">
                      <Button
                        variant="outlined"
                        color="error"
                        onClick={() => handleDelivery(row.id, row.deliver_to)}
                      >
                        deliver
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </div>
      </div>
    );
  }
}
