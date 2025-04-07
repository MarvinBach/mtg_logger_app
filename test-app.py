from supabase import create_client
import streamlit as st

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

try:
    response = supabase.table("players").insert({"name": "Mark"}).execute()
    st.write(f"Insert successful: {response}")
    entries = supabase.table("players").select("*").limit(10).execute()
    st.write("First 10 entries in the table:", entries.data)
except Exception as e:
    st.write(f"An error occurred: {e}")
