import './LoadingSpinner.css';

const LoadingSpinner = ({message}) => {
  return (
    // This container centers the spinner and the text.
    <div className="spinner-container">
      {/* This div is the actual animated spinner circle. */}
      <div className="loading-spinner"></div>
      <p>{message}</p>
    </div>
  );
};

export default LoadingSpinner;