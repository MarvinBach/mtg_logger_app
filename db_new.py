import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from supabase import create_client
import streamlit as st

# Get the Supabase credentials from Streamlit's secrets
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# Initialize the Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Use the Supabase client to get the PostgreSQL connection URL
# This assumes that Supabase is configured to use PostgreSQL
DATABASE_URL = f"postgresql://postgres:{SUPABASE_KEY}@{SUPABASE_URL}:5432/postgres"

# Create the engine with the new DATABASE_URL
engine = create_engine(DATABASE_URL, echo=True)

# Create the sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to initialize the database (creating tables)
def init_db():
    Base.metadata.create_all(bind=engine)
