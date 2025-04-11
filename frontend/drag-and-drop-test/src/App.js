import { useState } from "react";
import axios from "axios";

function App() {
  const [files, setFiles] = useState(null);
  const [progress, setProgress] = useState({ started: false, pc: 0 });
  const [msg, setMsg] = useState(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleUpload = () => {
    if (!files) {
      console.log("No file selected");
      return;
    }

    const fd = new FormData();
    for (let i = 0; i < files.length; i++) {
      fd.append(`file${i + 1}`, files[i]);
    }

    setMsg("Uploading...");
    setProgress((prevState) => ({ ...prevState, started: true }));
    axios
      .post("http://httpbin.org/post", fd, {
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
      })
      .catch((err) => {
        setMsg("Upload failed");
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
      </div>
    </div>
  );
}

export default App;
