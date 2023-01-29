import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
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

import "./delivery.css";

function Delivery({ islogged, setIsLogged, token, setToken }) {
  const [formState, setFormState] = useState("IN_PROGRESS");
  const [itemId, setitemIdState] = useState("");
  const [otp, setotpState] = useState("");
  const [result, setResultState] = useState("");
  const itemRef = useRef("");
  const otpRef = useRef("");
  const [userLat, setUserLat] = useState(0);
  const [userLong, setUserLong] = useState(0);

  const handleSubmission = () => {
    setitemIdState(itemRef.current.value);
    setotpState(otpRef.current.value);
    if (itemId && otp) {
      setFormState("FETCHING_DATA");
    }
  };

  useEffect(() => {
    navigator.geolocation.getCurrentPosition((position) => {
      setUserLat(position.coords.latitude);
      setUserLong(position.coords.longitude);
      console.log(userLat, userLong);
    });
  }, []);
  console.log(userLat);

  useEffect(() => {
    if (formState === "FETCHING_DATA") {
      axios
        .post(`https://46af-14-139-174-50.in.ngrok.io/person/login/`, {
          item_id: itemId,
          otp: otp,
          lat: userLat,
          lng: userLong,
        })
        .then((res) => {
          console.log(res);
          setFormState("DONE");
          setResultState(res.data);

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
          label="Item-ID"
          inputRef={itemRef}
          required="true"
        />
        <TextField
          InputLabelProps={{ style: { color: "red" }, shrink: true }}
          id="resultNo"
          label="OTP"
          inputRef={otpRef}
          //required="true"
        />
        <div>upload pic</div>

        <Button
          onClick={handleSubmission}
          variant="contained"
          style={{ width: "32ch" }}
        >
          Attempt Delivery
        </Button>
      </Box>
    );
  } else {
    if (formState === "FETCHING_DATA") {
      return (
        <div className="codeforces-id-input">
          <Typography variant="h5" component="div" color="Black" gutterBottom>
            Posting delivery attempt for {itemId}
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

export default Delivery;
