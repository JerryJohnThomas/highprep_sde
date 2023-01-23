
import React, { useState } from 'react';
import { Button, Input } from 'antd';

const ExcelUploader = ({uploadedExcel,setUploadedExcel}) => {
  const [uploadedFileName, setUploadedFileName] = useState();

  const handleFileChange = (e) => {
    const file = e.target.files[0];
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
        onChange={handleFileChange}
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