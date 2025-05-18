import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from sqlalchemy import text

from src.connection_to_db import create_dynamic_engine
from src.utils.logger import setup_logger
from src.utils.model import DataModel

# Initialize logger
logger = setup_logger(__name__)

# Create the FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load environment variables
load_dotenv()

MODEL = "gpt-3.5-turbo"


# Client will be initialized during startup event
client = None


@app.on_event("startup")
async def startup_event():
    global client
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        client = OpenAI(api_key=api_key)
        logger.info("OPENAI API Key connection is successful")
    except Exception as e:
        logger.error(f"Invalid API key: {e}")
        raise ValueError(f"Invalid API key: {e}") from e


@app.post("/chat")
async def chat(request: DataModel):
    global client
    try:
        # Validate input
        if not request or not hasattr(request, "string"):
            raise ValueError("Invalid request format. Must contain 'string' field.")

        user_input = request.string
        if not user_input:
            return {"error": "User input is required"}

        # Create engine from user's connection details
        engine = create_dynamic_engine()

        # Ask OpenAI to extract table names
        table_names_resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "Extract table names used in the prompt. Comma-separated, no explanation.",
                },
                {"role": "user", "content": user_input},
            ],
        )

        # Extract table names
        table_names_str = table_names_resp.choices[0].message.content.strip()
        table_names = [name.strip() for name in table_names_str.split(",") if name.strip()]

        logger.info(f"Extracted table names: {table_names}")

        # Generate SQL query
        sql_query_resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "Generate a SQL query based on the user's input and the given table names.",
                },
                {"role": "user", "content": f"Tables: {table_names_str}\nQuery: {user_input}"},
            ],
        )

        # Extract SQL query
        sql_query = sql_query_resp.choices[0].message.content.strip()

        # Remove any descriptive text and code block markers
        import re

        # Use regex to extract SQL query
        sql_match = re.search(r"SELECT.*?FROM.*?;", sql_query, re.DOTALL | re.IGNORECASE)
        if sql_match:
            sql_query = sql_match.group(0).strip()
        else:
            # Fallback to removing markers and stripping
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

        logger.info(f"Generated SQL query: {sql_query}")

        # Validate and execute query
        with engine.connect() as connection:
            try:
                logger.info(f"Executing SQL query: {sql_query}")
                result = connection.execute(text(sql_query))

                # Correct way to convert rows to dicts
                formatted_rows = [dict(row) for row in result.mappings().all()]

                return {"query": sql_query, "results": formatted_rows}
            except Exception as e:
                logger.error(f"Error executing query: {e}")
                return {"error": f"Error executing query: {e}"}

    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return {"error": str(e)}
