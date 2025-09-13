import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any

# This is the base schema that contains all the fields that might be
# associated with a resume. Other schemas will inherit from this to avoid repetition.
class ResumeBase(BaseModel):
    filename: str
    name: Optional[str] = None
    email: Optional[EmailStr] = None # Pydantic will validate this is a proper email format.
    phone: Optional[str] = None
    # We use 'Any' here because the structure of the JSON from the LLM can be flexible.
    extracted_data: Optional[Any] = None
    llm_analysis: Optional[Any] = None

# This schema is used when creating a new resume record.
# It's identical to the base for now, but having a separate class is good practice
# in case we want to add creation-specific fields later.
class ResumeCreate(ResumeBase):
    pass

# This is a lightweight schema designed for the "History" list view.
# It only includes the essential info needed to display a list of resumes,
# keeping the API response smaller and faster.
class ResumeSummary(BaseModel):
    id: int
    filename: str
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    uploaded_at: datetime.datetime

    # This little bit of config tells Pydantic it's okay to read data
    # directly from our SQLAlchemy ORM objects (e.g., resume.id instead of resume['id']).
    class Config:
        orm_mode = True

# This is the full resume schema, used when we need to send all the data
# for a single resume. It's used for the upload response and the "View Details" modal.
# It inherits from ResumeSummary and just adds the remaining fields.
class Resume(ResumeSummary):
    phone: Optional[str] = None
    extracted_data: Optional[Any] = None
    llm_analysis: Optional[Any] = None

    # It also needs orm_mode to work with SQLAlchemy objects.
    class Config:
        orm_mode = True
