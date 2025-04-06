import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

from dotenv import load_dotenv
load_dotenv(".env")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_PASSWORD = os.getenv("SUPABASE_PASSWORD")

if "db." not in SUPABASE_URL:
    SUPABASE_URL = f"db.{SUPABASE_URL}"

DATABASE_URL = f"postgresql://postgres:{SUPABASE_PASSWORD}@{SUPABASE_URL}:5432/postgres"


engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)



#-------------
#import streamlit as st
#SUPABASE_URL = st.secrets["supabase"]["url"]
#SUPABASE_PASSWORD = st.secrets["supabase"]["password"]
