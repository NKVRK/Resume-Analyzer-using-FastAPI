import './ErrorMessage.css';

// Just takes a 'message' string and displays it in a styled box.
const ErrorMessage = ({ message }) => {
  if (!message) {
    return null; // Don't render anything if there's no message.
  }

  return (
    <div className="error-message">
      <strong>Error:</strong> {message}
    </div>
  );
};

export default ErrorMessage;