import { useState } from "react";
import axios from "axios";

function App() {
  const [files, setFiles] = useState(null);
  const [progress, setProgress] = useState({ started: false, pc: 0 });
  const [msg, setMsg] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [downloadLink, setDownloadLink] = useState(null);
  const [jsonPreview, setJsonPreview] = useState(null);
  const [fileType, setFileType] = useState("supply_quote"); // Default file type
  const [customName, setCustomName] = useState(""); // Text box for custom name

  const handleUpload = () => {
    if (!files) {
      console.log("No file selected");
      return;
    }

// Reset JSON preview and download link
    setJsonPreview(null);
    setDownloadLink(null);

    const fd = new FormData();
    fd.append("file", files[0]);

    setMsg("Processing...");
    setProgress((prevState) => ({ ...prevState, started: true }));
    axios.post(`http://localhost:8000/upload/${fileType}`, fd, {
        onUploadProgress: (progressEvent) => {
          setProgress((prevState) => ({
            ...prevState,
            pc: Math.round((progressEvent.loaded * 100) / progressEvent.total),
          }));
        },
        headers: {
          "Custom-Header": "value",
        },
      })
      .then((res) => {
        setMsg("Process successful");
        console.log(res.data);

        // Extract the structured data from the response
        const { structured_data } = res.data;

        // Update the JSON preview state
        setJsonPreview(structured_data);

        // Create a downloadable JSON file
        const jsonBlob = new Blob([JSON.stringify(structured_data, null, 2)], { type: "application/json" });
        const downloadUrl = URL.createObjectURL(jsonBlob);

        // Set the download link with the custom name and file type
        const fileName = `${customName || "document"}_${fileType}.json`;
        const link = document.createElement("a");
        link.href = downloadUrl;
        link.download = fileName;
        link.click();

        setDownloadLink(downloadUrl);
      })
      .catch((err) => {
        setMsg(err.response?.data?.error || "Process failed");
        console.log(err);
      });
  };

  const handleCompanyUpload = () => {
    // Simulate uploading to the company's system
    setMsg("Uploading to Company system...");
  
    // Simulate a delay for the upload process
    setTimeout(() => {
      setMsg("Successfully uploaded to Company");
    }, 2000); // 2-second delay
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation(); // Prevent default behavior and stop propagation

    setIsDragging(false); // Reset the dragging state

    // Reset JSON preview and download link
    setJsonPreview(null);
    setDownloadLink(null);
    setMsg(null);

    // Get the dropped files
    const droppedFiles = Array.from(e.dataTransfer.files);

    // Filter files to only allow .png and .jpeg
    const validFiles = droppedFiles.filter((file) =>
      ["image/png", "image/jpeg", "text/csv", "application/pdf", "text/plain"].includes(file.type)
    );

    if (validFiles.length === 0) {
      setMsg("Only .png, .jpeg, .csv, .pdf, and .txt files are allowed");
      return;
    }

    setFiles(validFiles); // Update state with valid files
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    e.dataTransfer.dropEffect = "copy"; // Change the cursor to "copy"
    setIsDragging(true); // Keep the state active while hovering
  };

  const handleDragEnter = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true); // Set dragging state to true
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();

    // Only reset if the mouse leaves the entire dropzone
    if (e.relatedTarget === null || !e.currentTarget.contains(e.relatedTarget)) {
      setIsDragging(false);
    }
  };

  const handleDeleteFile = (index) => {
    const updatedFiles = Array.from(files); // Create a copy of the files array
    updatedFiles.splice(index, 1); // Remove the file at the specified index
    setFiles(updatedFiles); // Update the state with the new array
  };

  return (
    <div className="App">

      <div
        style={{
          padding: "0 20px",
          maxWidth: "12000px",
          margin: "0 auto", 
        }}
      >
      
      <h1><center>Document Processor</center></h1>

      {/* Dropdown for File Type */}
      <div style={{ marginBottom: "20px" }}>
        <label htmlFor="fileType" style={{ marginRight: "10px", marginLeft: "10px" }}>
          Select Document Type:
        </label>
        <select
          id="fileType"
          value={fileType}
          onChange={(e) => setFileType(e.target.value)}
          style={{ padding: "5px", borderRadius: "5px" }}
        >
          <option value="supply_quote">Supply Quote</option>
          <option value="supply_pricing_update">Supply Pricing Update</option>
          <option value="shipping_update">Shipping Update</option>
          <option value="vendor_invoice">Vendor Invoice</option>
        </select>
      </div>

      {/* Text Box for Custom Name */}
      <div style={{ marginBottom: "20px" }}>
        <label htmlFor="customName" style={{ marginRight: "10px",marginLeft: "10px" }}>
          Enter Vendor's Name:
        </label>
        <input
          id="customName"
          type="text"
          value={customName}
          onChange={(e) => setCustomName(e.target.value)}
          placeholder="Enter Vendor's name"
          style={{ padding: "5px", borderRadius: "5px", width: "200px" }}
        />
      </div>

      {/* Dropzone Area */}
      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        style={{
          border: isDragging ? "2px solid #007bff" : "2px dashed #007bff",
          backgroundColor: isDragging ? "#e6f7ff" : "#f9f9f9",
          borderRadius: "10px",
          padding: "20px",
          textAlign: "center",
          marginBottom: "20px",
          cursor: "pointer",
          transition: "background-color 0.3s ease, border 0.3s ease",
        }}
      >
        <p>Drag and drop files here, or click to select files</p>
        {isDragging && <p style={{ color: "#007bff" }}>Release to drop the files</p>}
        <input
          onChange={(e) => setFiles(e.target.files)}
          type="file"
          multiple
          accept=".png, .jpeg, .csv, .pdf, .txt"
          style={{ display: "none" }}
          id="fileInput"
        />
        <label
          htmlFor="fileInput"
          style={{
            display: "inline-block",
            padding: "10px 20px",
            backgroundColor: "#007bff",
            color: "#fff",
            borderRadius: "5px",
            cursor: "pointer",
          }}
        >
          Browse Files
        </label>
      </div>

      {/* File List */}
      {files && (
        <ul style={{ listStyleType: "none", padding: 0 }}>
          {Array.from(files).map((file, index) => (
            <li
              key={index}
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                marginBottom: "10px",
                padding: "5px 10px",
                border: "1px solid #ddd",
                borderRadius: "5px",
              }}
            >
              <span>{file.name}</span>
              <button
                onClick={() => handleDeleteFile(index)}
                style={{
                  backgroundColor: "red",
                  color: "white",
                  border: "none",
                  borderRadius: "50%",
                  width: "20px",
                  height: "20px",
                  cursor: "pointer",
                  textAlign: "center",
                  lineHeight: "20px",
                }}
              >
                X
              </button>
            </li>
          ))}
        </ul>
      )}

      {/* Process Button and Progress Bar */}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          marginTop: "20px",
        }}
      >
        <button onClick={handleUpload} className="upload-button">
          <i className="fas fa-upload" style={{ marginRight: "0px" }}></i>
          Process
        </button>

        {progress.started && (
          <progress
            max="100"
            value={progress.pc}
            style={{ display: "block", width: "50%", marginTop: "20px" }}
          ></progress>
        )}

        {msg && (
          <span style={{ marginTop: "10px", fontSize: "16px" }}>
            {msg}
          </span>
        )}

        {jsonPreview && (
          <div style={{ marginTop: "20px", padding: "10px", border: "1px solid #ddd", borderRadius: "5px" }}>
            <h3>JSON Preview:</h3>
            <pre>{JSON.stringify(jsonPreview, null, 2)}</pre>
          </div>
        )}

        {downloadLink && (
          <div style={{ marginTop: "20px", display: "flex", gap: "10px", alignItems: "center" }}>
            <a
              href={downloadLink}
              download={`${customName || "document"}_${fileType}.json`}
              style={{
                textDecoration: "none",
                color: "#007bff",
                fontWeight: "bold",
              }}
            >
              Download JSON File
            </a>
            <button onClick={handleCompanyUpload} className="upload-button">
              Upload to Company
            </button>
          </div>
        )}
      </div>
      </div>
    </div>
  );
}

export default App;