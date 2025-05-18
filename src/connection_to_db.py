import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

from src.utils.logger import setup_logger

logger = setup_logger(__name__)


# Create engine from user's connection details
def create_dynamic_engine():
    # Load environment variables at the start of the function
    load_dotenv()

    try:
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        dbname = os.getenv("DB_NAME")

        if not all([user, password, host, port, dbname]):
            raise ValueError("One or more required environment variables are missing.")

        # If host is localhost, try alternative connection methods
        if host in ["localhost", "127.0.0.1"]:
            logger.warning("Using localhost for database connection. Ensure PostgreSQL is running.")

        db_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
        return create_engine(db_url, connect_args={"connect_timeout": 10})
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise
