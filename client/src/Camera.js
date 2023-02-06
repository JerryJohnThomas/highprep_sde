// import React from 'react'

// function Camera() {
//   return (
//     <div>Camera</div>
//   )
// }

// export default Camera

// import React, { useState, useRef } from 'react';

// const Camera = () => {

//     const videoRef = useRef(null);
//     const canvasRef = useRef(null);
//     const [capturedImage, setCapturedImage] = useState(null);
  
//     const captureImage = () => {
//         const context = canvasRef.current.getContext("2d");
//         context.drawImage(videoRef.current, 0, 0, 400, 300);
//         setCapturedImage(canvasRef.current.toDataURL("image/jpg"));
//     };
  
//     return (
//       <div>
//         <video ref={videoRef} width="400" height="300" autoPlay={true}></video>
//         <button onClick={captureImage}>Capture</button>
//         {capturedImage && <img src={capturedImage} alt="captured" />}
//         <canvas ref={canvasRef} width="400" height="300"></canvas>
//       </div>
//     );
// };

// export default Camera;


//import React, { useState, useEffect } from 'react';
import React, { useRef, useEffect } from 'react';

const CaptureImageFromVideoCam = () => {
  const videoRef = useRef();
  const canvasRef = useRef();

  useEffect(() => {
    
    // get access to the camera
    //  { deviceId: { exact: 'second video feed id'} }
    // navigator.mediaDevices.getUserMedia({ video: { deviceId: { exact: '1'} } }).then(stream => {
        navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
      videoRef.current.srcObject = stream;
    });
  }, []);

  const capture = () => {
    const context = canvasRef.current.getContext('2d');
    context.drawImage(videoRef.current, 0, 0, canvasRef.current.width, canvasRef.current.height);
  };

  return (
    <div>
      <video ref={videoRef} width="320" height="240" autoPlay muted />
      <button onClick={capture}>Capture</button>
      <canvas ref={canvasRef} width="320" height="240" />
    </div>
  )
};


export default CaptureImageFromVideoCam;

