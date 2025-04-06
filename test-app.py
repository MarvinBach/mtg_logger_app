from supabase import create_client
import streamlit as st

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

try:
    response = supabase.table("players").insert({"name": "Marvin"}).execute()
    st.write(f"Insert successful: {response}")
except Exception as e:
    st.write(f"An error occurred: {e}")
