import React from "react";
import axios from "axios";
import "./camera2.css";
import Grid from "@mui/material/Grid";
import Button from "@mui/material/Button";

class Camera2 extends React.Component {
  constructor() {
    super();

    this.cameraNumber = 0;

    this.state = {
      imageDataURL: null,
      result: 0,
    };
  }

  initializeMedia = async () => {
    this.setState({ imageDataURL: null });

    if (!("mediaDevices" in navigator)) {
      navigator.mediaDevices = {};
    }

    if (!("getUserMedia" in navigator.mediaDevices)) {
      navigator.mediaDevices.getUserMedia = function (constraints) {
        var getUserMedia =
          navigator.webkitGetUserMedia || navigator.mozGetUserMedia;

        if (!getUserMedia) {
          return Promise.reject(new Error("getUserMedia Not Implemented"));
        }

        return new Promise((resolve, reject) => {
          getUserMedia.call(navigator, constraints, resolve, reject);
        });
      };
    }

    //Get the details of video inputs of the device
    const videoInputs = await this.getListOfVideoInputs();

    //The device has a camera
    if (videoInputs.length) {
      navigator.mediaDevices
        .getUserMedia({
          video: {
            deviceId: {
              exact: videoInputs[this.cameraNumber].deviceId,
            },
          },
        })
        .then((stream) => {
          this.player.srcObject = stream;
        })
        .catch((error) => {
          console.error(error);
        });
    } else {
      alert("The device does not have a camera");
    }
  };

  capturePicture = () => {
    var canvas = document.createElement("canvas");
    canvas.width = this.player.videoWidth;
    canvas.height = this.player.videoHeight;
    var contex = canvas.getContext("2d");
    contex.drawImage(this.player, 0, 0, canvas.width, canvas.height);
    this.player.srcObject.getVideoTracks().forEach((track) => {
      track.stop();
    });

    console.log(canvas.toDataURL());
    this.setState({ imageDataURL: canvas.toDataURL() });

    const imgData = canvas.toDataURL("image/png");
    console.log(imgData);
    canvas.toBlob(function (blob) {
      const formData = new FormData();
      formData.append("file1", blob, "filename.png");

      // Post via axios or other transport method
      axios
        .post(
          "http://057a-2409-40f4-102c-494f-c4cc-47b2-91a4-3be2.in.ngrok.io/algo/cv/",
          formData
        )
        .then((response) => response.text())
        .then((result) => console.log(result))
        .catch((error) => console.log("error", error));
    });

    // this.setState({ imageDataURL: canvas.toDataURL() });
    // formdata.append("file1", canvas.toDataURL(), "[PROXY]");
    // console.log(formdata);
    // //formdata.append("", fileInput.files[0], "[PROXY]");

    // var requestOptions = {
    //   method: "POST",
    //   body: formdata,
    //   redirect: "follow",
    // };

    // fetch(
    //   "https://057a-2409-40f4-102c-494f-c4cc-47b2-91a4-3be2.in.ngrok.io/algo/cv/",
    //   requestOptions
    // )
    //   .then((response) => response.text())
    //   .then((result) => console.log(result))
    //   .catch((error) => console.log("error", error));
  };

  switchCamera = async () => {
    const listOfVideoInputs = await this.getListOfVideoInputs();

    // The device has more than one camera
    if (listOfVideoInputs.length > 1) {
      if (this.player.srcObject) {
        this.player.srcObject.getVideoTracks().forEach((track) => {
          track.stop();
        });
      }

      // switch to second camera
      if (this.cameraNumber === 0) {
        this.cameraNumber = 1;
      }
      // switch to first camera
      else if (this.cameraNumber === 1) {
        this.cameraNumber = 0;
      }

      // Restart based on camera input
      this.initializeMedia();
    } else if (listOfVideoInputs.length === 1) {
      alert("The device has only one camera");
    } else {
      alert("The device does not have a camera");
    }
  };

  getListOfVideoInputs = async () => {
    // Get the details of audio and video output of the device
    const enumerateDevices = await navigator.mediaDevices.enumerateDevices();

    //Filter video outputs (for devices with multiple cameras)
    return enumerateDevices.filter((device) => device.kind === "videoinput");
  };
  getResult = async () => {
    //do get request
    this.setState({ result: 50 });
  };
  render() {
    const playerORImage = Boolean(this.state.imageDataURL) ? (
      <img src={this.state.imageDataURL} alt="cameraPic" />
    ) : (
      <video
        ref={(refrence) => {
          this.player = refrence;
        }}
        autoPlay
      ></video>
    );

    return (
      <div className="container">
        <div className="left">{playerORImage}</div>
        <div className="right">
          <Button
            style={{ width: "30ch", bold: true }}
            variant="contained"
            onClick={this.initializeMedia}
          >
            Live Feed
          </Button>
          <br></br>
          <Button
            variant="contained"
            color="error"
            onClick={this.capturePicture}
          >
            Click
          </Button>
          <br></br>
          <Button variant="contained" onClick={this.switchCamera}>
            Switch
          </Button>
          <br></br>
          <Button variant="outlined" color="error" onClick={this.getResult}>
            Get Volume
          </Button>
          <br></br>
          <Button variant="text">Volume={this.state.result}</Button>
        </div>
      </div>
    );
  }
}

export default Camera2;
