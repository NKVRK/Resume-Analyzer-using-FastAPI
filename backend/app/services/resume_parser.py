import pdfplumber
import google.generativeai as genai
import json
import time
import functools
from ..core.config import GEMINI_API_KEY

# Import specific exceptions for robust retry handling
from google.api_core import exceptions as google_api_exceptions


# --- Retry Decorator ---
def retry_with_backoff(retries=3, initial_delay=2, backoff_factor=2):
    """
    A decorator for retrying a function call with exponential backoff.

    This is super useful for external API calls. Sometimes the API is temporarily
    overloaded or has a hiccup. Instead of failing immediately, this will wait
    and try again a few times.

    This will retry on specific Google API exceptions that are often transient:
    - ResourceExhausted: Rate limit exceeded.
    - ServiceUnavailable: Temporary server-side issue.
    - DeadlineExceeded: Request timed out.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            for i in range(retries):
                try:
                    # Try to run the function (e.g., our API call)
                    return func(*args, **kwargs)
                except (
                    google_api_exceptions.ResourceExhausted,
                    google_api_exceptions.ServiceUnavailable,
                    google_api_exceptions.DeadlineExceeded
                ) as e:
                    # If we hit one of the specified errors, we don't give up yet.
                    print(f"LLM call failed with {type(e).__name__}, attempt {i + 1} of {retries}. Retrying in {delay}s...")
                    time.sleep(delay)
                    # Increase the delay for the next potential retry.
                    delay *= backoff_factor
            # If all retries fail, we finally give up and raise an exception.
            raise Exception(f"LLM call failed after {retries} retries.")
        return wrapper
    return decorator


# Configure the Gemini API with our key.
genai.configure(api_key=GEMINI_API_KEY)
# We're using the 'flash' model because it's fast and great for this kind of task.
model = genai.GenerativeModel('gemini-1.5-flash')

def parse_pdf_to_text(file_content: bytes) -> str:
    """Extracts text from a PDF file's content using pdfplumber."""
    import io
    text = ""
    # We use io.BytesIO to treat our in-memory file content like a real file.
    with pdfplumber.open(io.BytesIO(file_content)) as pdf:
        for page in pdf.pages:
            # Added a check for None to handle blank pages or pages with only images.
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# Apply our new retry decorator to both LLM calls.
@retry_with_backoff(retries=3, initial_delay=2)
def call_gemini_for_extraction(resume_text: str) -> dict:
    """
    Sends resume text to Gemini for structured data extraction.
    Now includes a retry mechanism for transient API errors and rate limits.
    """
    # This is our prompt engineering. We're telling the AI exactly what to do
    # and what format to use for the response. This is key to getting reliable JSON back.
    prompt = f"""
    Act as an expert HR recruiter and technical parser. Your task is to extract structured information from the following resume text and return it as a clean, valid JSON object. Do not include any explanatory text or markdown formatting around the JSON.

    The JSON object must have the following schema:
    {{
      "name": "string",
      "email": "string",
      "phone": "string",
      "location": "string",
      "summary": "string",
      "core_skills": ["string"],
      "soft_skills": ["string"],
      "experience": [
        {{
          "title": "string",
          "company": "string",
          "dates": "string",
          "description": "string"
        }}
      ],
      "education": [
        {{
          "degree": "string",
          "institution": "string",
          "year": "string"
        }}
      ]
    }}

    Resume Text:
    ---
    {resume_text}
    ---
    """
    try:
        response = model.generate_content(prompt)
        # Sometimes the model wraps the JSON in markdown, so we clean that up.
        json_text = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(json_text)
    except json.JSONDecodeError:
        # If the model gives us something that isn't valid JSON, we can't proceed.
        print("Error: LLM returned malformed JSON during extraction.")
        raise ValueError("Failed to get structured data from LLM due to malformed JSON.")
    except Exception as e:
        # Catch any other unexpected errors during the call.
        print(f"An unexpected error occurred during Gemini extraction call: {e}")
        # Re-raise the exception to be handled by the retry decorator or the API endpoint.
        raise e

@retry_with_backoff(retries=3, initial_delay=2)
def call_gemini_for_analysis(extracted_data: dict) -> dict:
    """
    Sends the extracted JSON data to Gemini for analysis and suggestions.
    This second call lets the AI focus on one task at a time, improving quality.
    """
    prompt = f"""
    Act as an expert career coach. Based on the provided resume data in JSON format, provide a critical analysis. 
    
    Return a JSON object with three keys: 
    1.  'resume_rating': A score from 1 to 10, where 10 is excellent.
    2.  'improvement_areas': A paragraph with actionable advice and specific examples on how to improve the resume.
    3.  'upskill_suggestions': A list of 3-5 relevant skills to learn, with a brief, compelling explanation for why each is valuable for the candidate's profile.

    JSON Resume Data:
    ---
    {json.dumps(extracted_data, indent=2)}
    ---
    """
    try:
        response = model.generate_content(prompt)
        # Same cleanup as before.
        json_text = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(json_text)
    except json.JSONDecodeError:
        print("Error: LLM returned malformed JSON during analysis.")
        raise ValueError("Failed to get analysis from LLM due to malformed JSON.")
    except Exception as e:
        print(f"An unexpected error occurred during Gemini analysis call: {e}")
        # Re-raise the exception to be handled by the retry decorator or the API endpoint
        raise e