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

    const fd = new FormData();
    fd.append("file", files[0]);

    setMsg("Uploading...");
    setProgress((prevState) => ({ ...prevState, started: true }));
    axios.post("http://localhost:8000/upload", fd, {
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
        setMsg("Upload successful");
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
        setMsg(err.response?.data?.error || "Upload failed");
        console.log(err);
      });
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation(); // Prevent default behavior and stop propagation

    setIsDragging(false); // Reset the dragging state

    // Get the dropped files
    const droppedFiles = Array.from(e.dataTransfer.files);

    // Filter files to only allow .png and .jpeg
    const validFiles = droppedFiles.filter((file) =>
      ["image/png", "image/jpeg"].includes(file.type)
    );

    if (validFiles.length === 0) {
      setMsg("Only .png and .jpeg files are allowed");
      return;
    }

    setFiles(validFiles); // Update state with valid files
    setMsg(null); // Clear any previous error message
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

  return (
    <div className="App">
      <h1>File Uploader</h1>

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
          Enter Customer Name:
        </label>
        <input
          id="customName"
          type="text"
          value={customName}
          onChange={(e) => setCustomName(e.target.value)}
          placeholder="Enter file name"
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
          accept=".png, .jpeg"
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
        <ul>
          {Array.from(files).map((file, index) => (
            <li key={index}>{file.name}</li>
          ))}
        </ul>
      )}

      {/* Upload Button and Progress Bar */}
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
          Upload
        </button>

        {progress.started && (
          <progress
            max="100"
            value={progress.pc}
            style={{ display: "block", width: "50%", marginTop: "20px" }}
          ></progress>
        )}

        {msg && <span style={{ marginTop: "10px", fontSize: "16px" }}>{msg}</span>}

        {jsonPreview && (
          <div style={{ marginTop: "20px", padding: "10px", border: "1px solid #ddd", borderRadius: "5px" }}>
            <h3>JSON Preview:</h3>
            <pre>{JSON.stringify(jsonPreview, null, 2)}</pre>
          </div>
        )}

        {downloadLink && (
          <a
            href={downloadLink}
            download={`${customName || "document"}_${fileType}.json`}
            style={{
              marginTop: "20px",
              display: "inline-block",
              textDecoration: "none",
              color: "#007bff",
              fontWeight: "bold",
            }}
          >
            Download JSON File
          </a>
        )}
      </div>
    </div>
  );
}

export default App;