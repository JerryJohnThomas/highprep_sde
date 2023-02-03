import React, {useState, useEffect,useRef} from "react";

//import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import { Button } from '@mui/material';
import axios from "../axios"
// import axios from 'axios';
import './itemInv.css'

function createData(name, calories, fat, carbs, protein) {
  return { name, calories, fat, carbs, protein };
}

const rows = [
  createData('Frozen yoghurt', 159, 6.0, 24, 4.0),
  createData('Ice cream sandwich', 237, 9.0, 37, 4.3),
  createData('Eclair', 262, 16.0, 24, 6.0),
  createData('Cupcake', 305, 3.7, 67, 4.3),
  createData('Gingerbread', 356, 16.0, 49, 3.9),
];

export default function BasicTable({ token, islogged }) {
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
                    .get(`/inventory/`)
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
                <h1>Inventory (change column names)</h1>
                <div>
                    <TableContainer component={Paper}>
                        <Table sx={{ minWidth: 650 }} aria-label="simple table">
                            <TableHead>
                                <TableRow>
                                    <TableCell>id (100g serving)</TableCell>
                                    <TableCell align="right">
                                        Item Name
                                    </TableCell>
                                    <TableCell align="right">
                                        Item Volume&nbsp;(g)
                                    </TableCell>
                                    {/* <TableCell align="right">Carbs&nbsp;(g)</TableCell>
            <TableCell align="right">Protein&nbsp;(g)</TableCell> */}
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {result.map((row) => (
                                    <TableRow
                                        key={row.id}
                                        sx={{
                                            "&:last-child td, &:last-child th":
                                                { border: 0 },
                                        }}
                                    >
                                        <TableCell component="th" scope="row">
                                            {row.id}
                                        </TableCell>
                                        <TableCell align="right">
                                            {row.item_name}
                                        </TableCell>
                                        <TableCell align="right">
                                            {row.item_volume}
                                        </TableCell>
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
