import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from supabase import create_client
import streamlit as st

# Get the Supabase credentials from Streamlit's secrets
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# Ensure SUPABASE_URL has the correct format (add https:// if missing)
if not SUPABASE_URL.startswith("http"):
    SUPABASE_URL = f"https://{SUPABASE_URL}"

# Construct the PostgreSQL connection URL, adding the default port 5432
DATABASE_URL = f"postgresql://postgres:{SUPABASE_KEY}@{SUPABASE_URL}:5432/postgres"

# Initialize the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a sessionmaker instance
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to initialize the database (create tables if they don't exist)
def init_db():
    Base.metadata.create_all(bind=engine)
