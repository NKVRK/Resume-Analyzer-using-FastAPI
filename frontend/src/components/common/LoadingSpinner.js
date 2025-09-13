import './LoadingSpinner.css';

const LoadingSpinner = () => {
  return (
    // This container centers the spinner and the text.
    <div className="spinner-container">
      {/* This div is the actual animated spinner circle. */}
      <div className="loading-spinner"></div>
      <p>Analyzing your resume...</p>
    </div>
  );
};

export default LoadingSpinner;