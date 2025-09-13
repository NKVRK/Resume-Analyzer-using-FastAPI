import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON
from .database import Base

class Resume(Base):
    """
    This class represents the 'resumes' table in our database.
    It stores all the information related to a single resume analysis.
    """
    __tablename__ = "resumes"

    # The unique ID for each resume entry. This is the primary key.
    id = Column(Integer, primary_key=True, index=True)
    
    # The original filename of the uploaded PDF, e.g., "JohnDoe_Resume.pdf".
    filename = Column(String, index=True)
    
    # The timestamp for when this record was created. Defaults to the current time.
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # --- Key Extracted Fields ---
    # We pull these out into their own columns for easier querying and display,
    # even though they are also present in the JSON blobs below.
    name = Column(String)
    email = Column(String)
    phone = Column(String)

    # --- JSON Data Blobs ---
    # A JSON column to store all the structured data extracted by the LLM,
    # like skills, experience, education, etc.
    extracted_data = Column(JSON)
    
    # A JSON column to store the qualitative analysis from the LLM,
    # like the rating, improvement areas, and upskill suggestions.
    llm_analysis = Column(JSON)   