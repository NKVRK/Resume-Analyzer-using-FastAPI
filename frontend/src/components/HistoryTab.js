import { useState, useEffect, useCallback } from 'react';
import { getResumes, deleteResume } from '../services/api';
import LoadingSpinner from './common/LoadingSpinner';
import ErrorMessage from './common/ErrorMessage';
import ResumeDetailModal from './ResumeDetailModal';
import { FiTrash2 } from 'react-icons/fi';


const HistoryTab = ({ active }) => {
  // Holds the list of resumes fetched from the server.
  const [resumes, setResumes] = useState([]);

  // Shows a spinner while we're fetching data.
  const [isLoading, setIsLoading] = useState(true);

  // Stores any error message if something goes wrong.
  const [error, setError] = useState(null);

  // Keeps track of which resume is selected to show the details modal.
  const [selectedResumeId, setSelectedResumeId] = useState(null);

  // This function fetches the resume list from our API.
  // We wrap it in useCallback so it doesn't get recreated on every render,
  // which is important because we use it in a useEffect hook.
  const fetchResumes = useCallback(async () => {
    try {
      setIsLoading(true);
      const response = await getResumes();
      setResumes(response.data);
    } catch (err) {
      // If the API call fails, we'll show an error message.
      setError('Failed to fetch submission history.');
      console.error(err); // Also log the actual error for debugging.
    } finally {
      // Always stop the loading spinner, whether it succeeded or failed.
      setIsLoading(false);
    }
  }, []);

  // This effect runs when the component first loads and whenever the 'active' prop changes.
  useEffect(() => {
    // We only want to fetch data if this tab is actually visible.
    if (active) {
      fetchResumes();
    }
  }, [active, fetchResumes]);

  // When a user clicks "View Details", we set the selected resume ID to open the modal.
  const handleDetailsClick = (id) => {
    setSelectedResumeId(id);
  };

  // To close the modal, we just reset the selected ID back to null.
  const handleCloseModal = () => {
    setSelectedResumeId(null);
  };

  // Handles deleting a resume entry.
  const handleDelete = async (id, filename) => {
    // It's good practice to confirm with the user before a destructive action.
    if (window.confirm(`Are you sure you want to delete the resume "${filename}"?`)) {
      try {
        await deleteResume(id);
        // After successful deletion, we update the UI by removing the item from our state.
        // This is faster than re-fetching the whole list.
        setResumes(currentResumes => currentResumes.filter(r => r.id !== id));
      } catch (err) {
        setError(`Failed to delete resume. Please try again.`);
      }
    }
  };

  // Show a loading spinner while data is being fetched.
  if (isLoading) return <LoadingSpinner message="Loading submission history..." />;

  // If there was an error, show the error message instead of the table.
  if (error && resumes.length === 0) return <ErrorMessage message={error} />;

  return (
    <div className="tab-content">
      <h2>Submission History</h2>
      {/* Show a small error message at the top if something fails, e.g., deletion */}
      {error && <ErrorMessage message={error} />}
      
      {/* If there are no resumes, show a friendly message. */}
      {resumes.length === 0 && !isLoading ? (
        <p>You have not analyzed any resumes yet.</p>
      ) : (
        // Otherwise, display the table of resumes.
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Filename</th>
                <th>Name</th>
                <th>Uploaded At</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {resumes.map((resume) => (
                <tr key={resume.id}>
                  <td>{resume.filename}</td>
                  <td>{resume.name || 'N/A'}</td>
                  <td>{new Date(resume.uploaded_at).toLocaleString()}</td>
                  <td className="actions-cell">
                    <button onClick={() => handleDetailsClick(resume.id)}>
                      View Details
                    </button>
                    <button 
                      className="delete-button" 
                      onClick={() => handleDelete(resume.id, resume.filename)}
                    >
                      <FiTrash2 /> Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* The modal is only rendered in the DOM when a resume is selected. */}
      {selectedResumeId && (
        <ResumeDetailModal
          resumeId={selectedResumeId}
          onClose={handleCloseModal}
        />
      )}
    </div>
  );
};

export default HistoryTab;