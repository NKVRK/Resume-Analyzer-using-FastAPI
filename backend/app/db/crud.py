from sqlalchemy.orm import Session
from . import models
from ..schemas import resume as resume_schema

def get_resume(db: Session, resume_id: int):
    """
    Fetches a single resume from the database by its primary key (ID).
    """
    return db.query(models.Resume).filter(models.Resume.id == resume_id).first()

def get_resumes(db: Session, skip: int = 0, limit: int = 100):
    """
    Fetches a list of resumes from the database.
    Supports pagination with `skip` and `limit` parameters.
    """
    # This query gets all resumes, then applies offset and limit for pagination.
    return db.query(models.Resume).order_by(models.Resume.id.desc()).offset(skip).limit(limit).all()

def create_resume(db: Session, resume_data: dict):
    """
    Creates a new resume record in the database.
    """
    # We unpack the dictionary of data directly into our SQLAlchemy model.
    # This is a neat way to create the object as long as the keys match the model's attributes.
    db_resume = models.Resume(**resume_data)
    
    # Add the new resume object to the session (staging it for saving).
    db.add(db_resume)
    
    # Commit the transaction to actually save it to the database.
    db.commit()
    
    # Refresh the object to get any new data from the DB, like the auto-generated ID.
    db.refresh(db_resume)
    
    return db_resume

def delete_resume(db: Session, resume_id: int):
    """
    Deletes a resume from the database by its ID.
    """
    # First, we need to find the resume we want to delete.
    db_resume = db.query(models.Resume).filter(models.Resume.id == resume_id).first()
    
    # Only proceed if we actually found a resume with that ID.
    if db_resume:
        db.delete(db_resume)
        db.commit()
        # It's good practice to return the object that was deleted,
        # in case the caller wants to do something with it (like logging its filename).
        return db_resume
        
    # If no resume was found, we just return None.
    return None