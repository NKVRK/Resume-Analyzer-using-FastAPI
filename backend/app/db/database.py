from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# We're using SQLite for simplicity. The database will be a single file
# named 'resume_analyzer.db' in the root of the backend directory.
DATABASE_URL = "sqlite:///./resume_analyzer.db"

# The 'engine' is the core interface to the database. It's how SQLAlchemy
# communicates with our DB using the DATABASE_URL.
# The 'connect_args' is a specific requirement for SQLite to allow it to be
# used by multiple threads, which is how FastAPI handles requests.
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# A SessionLocal is a factory for creating new database sessions.
# Think of a session as a temporary "workspace" for all the database
# queries and operations related to a single API request.
SessionalLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# We create a 'Base' class here. Any of our database models (like the Resume model)
# will inherit from this class, which lets SQLAlchemy know about them.
Base = declarative_base()

# --- Dependency for API Endpoints ---
def get_db():
    """
    This is a FastAPI dependency that creates and yields a new database session
    for each incoming request. It also ensures the session is properly closed
    after the request is finished, even if an error occurs.
    """
    db = SessionalLocal()
    try:
        # 'yield' passes the session object to the API endpoint function.
        yield db
    finally:
        # This 'finally' block guarantees that the session is closed,
        # which is crucial for releasing database connections.
        db.close()