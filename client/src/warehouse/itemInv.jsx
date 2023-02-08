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
//import axios from "../axios";
import axios from "axios";
import "./itemInv.css";

function createData(id, weight, volume) {
  return { id, weight, volume };
}

const rows = [
  createData(1, 100, 10, "sharma Ji,xyz"),
  createData(2, 10, 5, "mehta Ji,xyz"),
  createData(3, 1200, 12, "raita Ji,xyz"),
  createData(4, 1040, 20, "tun tun Ji,xyz"),
  createData(5, 110, 7, "ladoo Ji,xyz"),
];

export default function BasicTable({ token, islogged }) {
  console.log("bro");
  const [formState, setFormState] = useState("FETCHING_DATA");
  const [result, setResultState] = useState("");

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

  useEffect(() => {
    if (formState === "FETCHING_DATA") {
      // .get(
      // `https://0e50-27-63-208-221.in.ngrok.io/inventory/`
      // )
      axios
        .get("https://28cf-2401-4900-647e-d5d2-c4cc-47b2-91a4-3be2.in.ngrok.io/")
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
  if (formState === "DONE") {
    return (
      <div className="layer1">
        <h1>Inventory</h1>
        <div>
          <TableContainer component={Paper}>
            <Table sx={{ minWidth: 650 }} aria-label="simple table">
              <TableHead>
                <TableRow>
                  <TableCell>id</TableCell>
                  <TableCell align="right">Item weight</TableCell>
                  <TableCell align="right">Item Volume</TableCell>
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
                    <TableCell align="right">{row.weight}</TableCell>
                    <TableCell align="right">{row.volume}</TableCell>
                    {/* <TableCell align="right">{row.carbs}</TableCell>
              <TableCell align="right">{row.protein}</TableCell> */}
                    <TableCell align="center">
                      <Button
                        variant="outlined"
                        color="error"
                        //   onClick={() => handleDelete(postIndex)}
                      >
                        remove
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
