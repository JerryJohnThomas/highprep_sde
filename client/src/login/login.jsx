import React, { useState, useEffect, useRef } from "react";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import RadioGroup from "@mui/material/RadioGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import FormControl from "@mui/material/FormControl";
import FormLabel from "@mui/material/FormLabel";
import Box from "@mui/material/Box";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import Select, { SelectChangeEvent } from "@mui/material/Select";
import LinearProgress from "@mui/material/LinearProgress";
import Typography from "@mui/material/Typography";
import { useNavigate } from "react-router-dom";
import "./login.css";
// import axios from "axios";
import axios from "../axios"

function Login({ query, setQueryState, islogged, setIsLogged, token, setToken }) {
    const [formState, setFormState] = useState("IN_PROGRESS");
    const [model, setModelState] = useState("BM25");
    const [resultNo, setResultNoState] = useState("");
    const [result, setResultState] = useState("");
    const queryRef = useRef("");
    const modelRef = useRef("");
    const resultNoRef = useRef("");

    const handleSubmission = () => {
        setQueryState(queryRef.current.value);
        setModelState(modelRef.current.value);
        setResultNoState(resultNoRef.current.value);
        if (query && model && resultNo) {
            setFormState("FETCHING_DATA");
        }
    };

    const navigate = useNavigate();
    useEffect(() => {
        if (formState === "FETCHING_DATA") {
            axios
                .post(`/api-token-auth/`, {
                    // email: query,
                    username: query,
                    password: resultNo,
                })
                .then((res) => {
                    console.log(res);
                    setFormState("DONE");
                    setResultState(res.data);

                    if (res.status == 200) {
                        setIsLogged(true);
                        console.log(res.data.token);
                        // setToken(() => res.data.token); // this should be the token
                        setToken(res.data.token); // this should be the token

                        // TO DO @shub
                        // check if user is warehouse like that ...
                        if (modelRef.current=="U2")
                            navigate("/warehouse/", { replace: true });
                        else if (modelRef.current == "U1")
                            navigate("/rider/maps", { replace: true });

                    }

                    // else if (res.status == 400)
                    // {
                    //     setFormState("ERROR");
                    //     console.log("error");
                    // }
                    // TO DO @shub
                    //if(res!=iNVALID)
                    // {
                    // setIsLogged(true);
                    // setToken(res.data."")            // this should be the token
                    // }
                })
                .catch((error) => {
                    setFormState("ERROR");
                    console.log(error);
                });
        }
    }, [formState]);

    if (formState === "IN_PROGRESS") {
        //return simple form page
        // return(
        //   <>
        //   <TextField id="outlined-basic" label="Outlined" variant="outlined" inputRef={queryRef} />
        //   <TextField id="outlined-basic" label="Outlined" variant="outlined" inputRef={modelRef}/>
        //   <TextField id="outlined-basic" label="Outlined" variant="outlined" inputRef={resultNoRef}/>
        //   <Button
        //       onClick={handleSubmission}
        //       variant="contained"
        //       style={{width: "32ch"}}
        //     > Submit </Button>
        //   </>
        // )
        return (
            <Box
                component="form"
                sx={{
                    "& > :not(style)": { m: 1, width: "25ch" },
                }}
                className="codeforces-id-input"
            >
                <TextField
                    InputLabelProps={{ style: { color: "red" } }}
                    id="Query"
                    label="User-ID"
                    inputRef={queryRef}
                    required="true"
                />
                <TextField
                    InputLabelProps={{ style: { color: "red" }, shrink: true }}
                    id="resultNo"
                    label="Password"
                    type="password"
                    inputRef={resultNoRef}
                    required="true"
                />
                <FormControl fullWidth>
                    <InputLabel id="demo-simple-select-label">
                        User Type
                    </InputLabel>
                    <Select
                        labelId="demo-simple-select-label"
                        inputRef={modelRef}
                        //value={age}
                        label="Age"
                        //onChange={handleChange}
                    >
                        <MenuItem value="U3">Customer</MenuItem>
                        <MenuItem value="U2">Rider</MenuItem>
                        <MenuItem value="U1">Warehouse guy</MenuItem>
                        <MenuItem value="U0">The Boss</MenuItem>
                    </Select>
                </FormControl>

                <Button
                    onClick={handleSubmission}
                    variant="contained"
                    style={{ width: "32ch" }}
                >
                    Submit
                </Button>
            </Box>
        );
    } else {
        if (formState === "FETCHING_DATA") {
            return (
                <div className="codeforces-id-input">
                    <Typography
                        variant="h5"
                        component="div"
                        color="Black"
                        gutterBottom
                    >
                        Loading data for {query}
                    </Typography>
                    <Box sx={{ width: "50%" }}>
                        <LinearProgress />
                    </Box>
                </div>
            );
        }
    }

    return (
        <div className="App">
            <div className="results">
                {result.map((res, i) => {
                    const url = `${res.URL}`;
                    return (
                        <div className="result" key={i}>
                            <h3>{res.Title}</h3>
                            <p
                                dangerouslySetInnerHTML={{
                                    __html: res.Summary,
                                }}
                            ></p>
                            <a href={url} target="_blank" rel="noreferrer">
                                Read more
                            </a>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}

export default Login;
