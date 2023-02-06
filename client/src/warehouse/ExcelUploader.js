
import React, { useState } from 'react';
import { Button, Input } from 'antd';
import { useEffect } from 'react';

const ExcelUploader = ({uploadedExcel,setUploadedExcel}) => {
  useEffect(()=>{
    setUploadedExcel(null);
  },[])
  
  const [uploadedFileName, setUploadedFileName] = useState();


  const handleFileChange = (e) => {
    const file = e.target.files[0];
    console.log(file);
    setUploadedExcel(file);
    setUploadedFileName(file.name);
  };

  const handleClearFile = () => {
    setUploadedExcel(null);
    setUploadedFileName("No File Choosen");
  };

  return (
    <div>
      <Input
        type="file"
        onChange={(e)=>handleFileChange(e)}
        accept=".xlsx, .xls, .csv"
      />
      {uploadedFileName && (
        <div style={{marginTop:"20px"}}>
          <span>{uploadedFileName}  <span></span> <span></span>  </span>
          <Button onClick={handleClearFile} >Clear</Button>
        </div>
      )}
    </div>
  );
};

export default ExcelUploader;