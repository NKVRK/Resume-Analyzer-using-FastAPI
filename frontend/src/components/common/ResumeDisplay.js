import './ResumeDisplay.css';
// Using some nice icons to make the UI a bit more engaging.
import { FiStar, FiThumbsDown, FiZap, FiInfo, FiMail, FiPhone, FiMapPin } from 'react-icons/fi';

const ResumeDisplay = ({ resumeData }) => {
  // If there's no data, don't render anything.
  if (!resumeData) return null;

  // Destructure the data to make it easier to work with.
  const { extracted_data, llm_analysis } = resumeData;

  // A quick sanity check to make sure we have the data we need.
  if (!extracted_data || !llm_analysis) {
    return <p>Analysis data is incomplete.</p>;
  }
  
  // This is a CSS variable trick to pass the rating score to the stylesheet
  // for the circular progress bar.
  const ratingStyle = { '--rating': llm_analysis.resume_rating };

  return (
    <div className="resume-display">
      {/* Use the candidate's name if we found it, otherwise fall back to the filename. */}
      <h2>Analysis for {extracted_data.name || resumeData.filename}</h2>

      {/* The big rating card at the top */}
      <div className="card rating-card">
        <h3><FiStar /> Overall Rating</h3>
        <div className="rating-circle" style={ratingStyle}>
          <div className="rating-score">
            {llm_analysis.resume_rating}<span style={{fontSize: '1.2rem', marginLeft: '4px'}}>/10</span>
          </div>
        </div>
      </div>
      
      {/* A two-column grid for the main analysis points */}
      <div className="display-grid">
        <div className="card">
          <h3><FiThumbsDown /> Areas for Improvement</h3>
          <p>{llm_analysis.improvement_areas}</p>
        </div>

        <div className="card">
          <h3><FiZap /> Upskill Suggestions</h3>
          <ul>
            {llm_analysis.upskill_suggestions.map((suggestion, index) => (
              <li key={index}>
                <strong>{suggestion.skill}:</strong> {suggestion.reason}
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* A full-width card for all the raw info we extracted */}
      <div className="card">
        <h3><FiInfo /> Extracted Information</h3>
        
        <h4>Contact Details</h4>
        <div className="contact-info-grid">
          {/* Conditionally render each piece of contact info only if it exists */}
          {extracted_data.email && (
            <div className="info-item">
              <FiMail size={20} className="info-icon" />
              <span>{extracted_data.email}</span>
            </div>
          )}
          {extracted_data.phone && (
            <div className="info-item">
              <FiPhone size={20} className="info-icon" />
              <span>{extracted_data.phone}</span>
            </div>
          )}
           {extracted_data.location && (
            <div className="info-item">
              <FiMapPin size={20} className="info-icon" />
              <span>{extracted_data.location}</span>
            </div>
          )}
        </div>

        <h4 style={{marginTop: '25px'}}>Core Skills</h4>
        <div className="skills-container">
          {extracted_data.core_skills.map((skill, index) => (
            <span key={index} className="skill-tag">{skill}</span>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ResumeDisplay;