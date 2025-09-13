import { useState, useEffect } from 'react';
import { getResumeById } from '../services/api';
import LoadingSpinner from './common/LoadingSpinner';
import ErrorMessage from './common/ErrorMessage';
import ResumeDisplay from './common/ResumeDisplay';
import './ResumeDetailModal.css';

// It takes the ID of the resume to show and a function to call when it should close.
const ResumeDetailModal = ({ resumeId, onClose }) => {
  // Holds the detailed resume data once it's fetched.
  const [resumeData, setResumeData] = useState(null);
  // Shows a spinner while we're fetching.
  const [isLoading, setIsLoading] = useState(true);
  // Catches any errors during the API call.
  const [error, setError] = useState(null);

  // This effect runs whenever the resumeId changes.
  useEffect(() => {
    if (resumeId) {
      const fetchResumeDetails = async () => {
        setIsLoading(true);
        setError(null);
        try {
          // Fetch the specific resume from the backend.
          const response = await getResumeById(resumeId);
          setResumeData(response.data);
        } catch (err) {
          console.error("Failed to fetch resume details:", err);
          setError('Could not load the resume details. Please try again.');
        } finally {
          // Always stop loading, whether it worked or not.
          setIsLoading(false);
        }
      };
      fetchResumeDetails();
    }
  }, [resumeId]); // The dependency array ensures this runs only when resumeId changes.

  return (
    // The dark background. Clicking it closes the modal.
    <div className="modal-overlay" onClick={onClose}>
      {/* The actual modal content. We stop clicks here from closing the modal. */}
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close-button" onClick={onClose}>×</button>
        
        {/* Show the right content based on the current state */}
        {isLoading && <LoadingSpinner />}
        {error && <ErrorMessage message={error} />}
        {resumeData && <ResumeDisplay resumeData={resumeData} />}
      </div>
    </div>
  );
};

export default ResumeDetailModal;