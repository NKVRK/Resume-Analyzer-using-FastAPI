from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List

from ...db import crud
from ...db.database import get_db
from ...schemas import resume as resume_schema
from ...services import resume_parser

router = APIRouter()

# Set a max file size for uploads to prevent abuse. 5MB should be plenty for a PDF resume.
MAX_FILE_SIZE_MB = 5
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


@router.post("/upload", response_model=resume_schema.Resume)
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    The main endpoint for uploading and analyzing a resume.
    It's a multi-step process:
    1. Validate the file (PDF, size limit).
    2. Parse the PDF to raw text.
    3. Make two calls to the Gemini LLM for extraction and analysis.
    4. Save the results to the database.
    5. Return the complete analysis to the client.
    """
    # First, basic validation. We only want PDF files.
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF is accepted.")
    
    try:
        # Read the file content into memory.
        file_content = await file.read()

        # Now, check if the file is too large.
        if len(file_content) > MAX_FILE_SIZE_BYTES:
            raise HTTPException(
                status_code=413, # 413: Payload Too Large
                detail=f"File size exceeds the limit of {MAX_FILE_SIZE_MB} MB."
            )
        
        # Step 1: Parse the PDF content to get plain text.
        resume_text = resume_parser.parse_pdf_to_text(file_content)
        if not resume_text.strip():
            # This can happen if the PDF is just an image or is blank.
            raise HTTPException(status_code=400, detail="Could not extract text from PDF. The file might be empty or image-based.")

        # Step 2: Use the LLM to pull out structured data like name, email, skills, etc.
        extracted_data = resume_parser.call_gemini_for_extraction(resume_text)

        # Step 3: Use the LLM again, this time for qualitative analysis and suggestions.
        llm_analysis = resume_parser.call_gemini_for_analysis(extracted_data)

        # Step 4: Bundle up all the data we want to save in the database.
        resume_data_to_save = {
            "filename": file.filename,
            "name": extracted_data.get("name"),
            "email": extracted_data.get("email"),
            "phone": extracted_data.get("phone"),
            "extracted_data": extracted_data,
            "llm_analysis": llm_analysis
        }

        # Step 5: Pass the data to our CRUD function to create the DB record.
        db_resume = crud.create_resume(db, resume_data=resume_data_to_save)
        return db_resume

    except ValueError as e:
        # This might happen if the LLM returns data in an unexpected format.
        raise HTTPException(status_code=500, detail=f"LLM processing error: {str(e)}")
    except HTTPException as e:
        # If we raised an HTTPException ourselves, just let it pass through.
        # This prevents it from being caught by the generic Exception handler below.
        raise e
    except Exception as e:
        # This is a catch-all for other problems, like if the LLM service is down
        # and all our retries (from the decorator) have failed.
        raise HTTPException(status_code=503, detail=f"Service unavailable after multiple retries: {str(e)}")


@router.get("/resumes", response_model=List[resume_schema.ResumeSummary])
def get_all_resumes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Fetches a summary of all previously analyzed resumes for the "History" tab.
    """
    resumes = crud.get_resumes(db, skip=skip, limit=limit)
    return resumes


@router.get("/resumes/{resume_id}", response_model=resume_schema.Resume)
def get_resume_details(resume_id: int, db: Session = Depends(get_db)):
    """
    Fetches the full, detailed analysis for a single resume by its ID.
    Used when the user clicks "View Details" on a resume in the history.
    """
    db_resume = crud.get_resume(db, resume_id=resume_id)
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    return db_resume

@router.delete("/resumes/{resume_id}", status_code=status.HTTP_200_OK)
def delete_resume_entry(resume_id: int, db: Session = Depends(get_db)):
    """
    Deletes a specific resume entry by its ID.
    """
    deleted_resume = crud.delete_resume(db, resume_id=resume_id)
    if deleted_resume is None:
        # Can't delete something that doesn't exist.
        raise HTTPException(status_code=404, detail="Resume not found")
    return {"ok": True, "message": f"Resume '{deleted_resume.filename}' deleted successfully."}