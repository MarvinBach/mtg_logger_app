#import os
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

#from dotenv import load_dotenv
#load_dotenv(".env")
#SUPABASE_URL = os.getenv("SUPABASE_URL")
#SUPABASE_PASSWORD = os.getenv("SUPABASE_PASSWORD")

#SUPABASE_URL = st.secrets["supabase"]["url"]
#SUPABASE_PASSWORD = st.secrets["supabase"]["password"]

#if "db." not in SUPABASE_URL:
#    SUPABASE_URL = f"db.{SUPABASE_URL}"

#DATABASE_URL = f"postgresql://postgres:{SUPABASE_PASSWORD}@{SUPABASE_URL}:5432/postgres"

from supabase import create_client

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

response = supabase.table("games").select("*").limit(1).execute()
st.write(response.data)


#engine = create_engine(DATABASE_URL, echo=True)
#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#def init_db():
#    Base.metadata.create_all(bind=engine)
