import { useState, useRef } from 'react';
import { uploadResume } from '../services/api';
import LoadingSpinner from './common/LoadingSpinner';
import ErrorMessage from './common/ErrorMessage';
import ResumeDisplay from './common/ResumeDisplay';
import { FiUpload, FiFile, FiCheckCircle, FiRotateCcw, FiX } from 'react-icons/fi';
import './UploadTab.css';

const UploadTab = () => {
  // Holds the file object the user has selected.
  const [selectedFile, setSelectedFile] = useState(null);
  // True when we're waiting for the API to respond.
  const [isLoading, setIsLoading] = useState(false);
  // Stores any error message to show to the user.
  const [error, setError] = useState(null);
  // Stores the successful analysis data from the backend.
  const [analysisResult, setAnalysisResult] = useState(null);
  // Tracks if a file is being dragged over the drop zone for styling.
  const [isDragging, setIsDragging] = useState(false);
  // A ref to the hidden file input so we can clear it programmatically.
  const fileInputRef = useRef(null);

  // Resets the entire component to its initial state, ready for a new upload.
  const handleReset = () => {
    setSelectedFile(null);
    setAnalysisResult(null);
    setError(null);
    // This is important to allow selecting the same file again after resetting.
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  // Central function to handle and validate a selected file, used by both
  // the file input and the drag-and-drop handler.
  const handleFileSelect = (file) => {
    // Make sure it's a PDF before we accept it.
    if (file && file.type === "application/pdf") {
      setError(null); // Clear any previous errors
      setAnalysisResult(null); // Clear old results
      setSelectedFile(file);
    } else if (file) {
      // If it's not a PDF, show an error.
      setError("Please select a valid PDF file.");
      setSelectedFile(null);
    }
  };

  // Clears the selected file before submitting for analysis.
  const handleRemoveFile = () => {
    setSelectedFile(null);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  // This is just the event handler for the hidden file input.
  const handleFileChange = (event) => {
    handleFileSelect(event.target.files[0]);
  };

  // Kicks off the analysis when the user clicks the submit button.
  const handleSubmit = async (event) => {
    event.preventDefault(); // Don't let the form refresh the page.
    if (!selectedFile) {
      setError('Please select a PDF file to upload.');
      return;
    }
    
    // Set loading state and clear out old data.
    setIsLoading(true);
    setError(null);
    setAnalysisResult(null);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await uploadResume(formData);
      setAnalysisResult(response.data);
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'An unexpected error occurred.';
      setError(errorMessage);
    } finally {
      // Always turn off the spinner, success or fail.
      setIsLoading(false);
    }
  };

  // --- Drag and Drop Event Handlers ---
  const handleDragOver = (event) => {
    event.preventDefault(); // This is necessary to allow a drop.
    setIsDragging(true);
  };

  const handleDragLeave = (event) => {
    event.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    setIsDragging(false);
    // Get the dropped file and run it through our validation function.
    handleFileSelect(event.dataTransfer.files[0]);
  };
  
  return (
    <div className="tab-content">
      {/* The view changes completely depending on if we have results or not. */}
      {!analysisResult ? (
        // --- UPLOAD VIEW ---
        <>
          <h2>Upload Your Resume</h2>
          <p>Drag and drop or select a PDF file to get an instant AI-powered analysis.</p>
          <form 
            onSubmit={handleSubmit} 
            className={`upload-form ${isDragging ? 'dragging' : ''}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
          >
            <FiUpload size={50} className="upload-icon" />
            
            {/* Show the selected file info or the upload instructions. */}
            {selectedFile ? (
              <div className="file-selected-message">
                <div className="file-info">
                  <FiCheckCircle size={20} color="green" />
                  <strong>{selectedFile.name}</strong>
                  <button type="button" onClick={handleRemoveFile} className="remove-file-button" title="Remove file">
                    <FiX />
                  </button>
                </div>
                <button type="submit" disabled={isLoading}>
                  {isLoading ? 'Analyzing...' : 'Analyze Resume'}
                </button>
              </div>
            ) : (
              <div className="upload-instructions">
                <label htmlFor="file-upload" className="file-input-label">
                  Select PDF
                </label>
                <input id="file-upload" type="file" accept=".pdf" onChange={handleFileChange} ref={fileInputRef} />
                <p>or drag and drop it here</p>
              </div>
            )}
          </form>
        </>
      ) : (
        // --- RESULTS VIEW ---
        <div className="results-container">
          <div className="results-header">
            <h2>Analysis Complete</h2>
            <button onClick={handleReset} className="reset-button">
              <FiRotateCcw /> Upload Another Resume
            </button>
          </div>
          <ResumeDisplay resumeData={analysisResult} />
        </div>
      )}

      {/* These are shown outside the main conditional so they can overlay the content. */}
      {isLoading && <LoadingSpinner />}
      {error && <ErrorMessage message={error} />}
    </div>
  );
};

export default UploadTab;