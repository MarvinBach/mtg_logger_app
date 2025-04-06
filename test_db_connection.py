import os
from sqlalchemy import create_engine, text  # Import the `text` function for raw SQL queries

from dotenv import load_dotenv
load_dotenv(".env")  # Load environment variables from .env file

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_PASSWORD = os.getenv("SUPABASE_PASSWORD")
print("SUPABASE_URL:", SUPABASE_URL)
print("SUPABASE_PASSWORD:", SUPABASE_PASSWORD)

DATABASE_URL = f"postgresql://postgres:{SUPABASE_PASSWORD}@db.{SUPABASE_URL}:5432/postgres"

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))  # Use `text()` to execute the raw SQL query
        print("✅ Connection successful:", result.scalar())  # `scalar()` retrieves the first column of the first row
except Exception as e:
    print("❌ Connection failed:", e)
