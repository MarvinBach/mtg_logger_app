import streamlit as st
from supabase import create_client
from typing import Optional

class DatabaseConfig:
    _instance: Optional['DatabaseConfig'] = None
    _client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConfig, cls).__new__(cls)
        return cls._instance

    @property
    def client(self):
        if self._client is None:
            try:
                self._client = create_client(
                    st.secrets["SUPABASE_URL"],
                    st.secrets["SUPABASE_KEY"]
                )
            except Exception as e:
                st.error(f"Failed to connect to database: {str(e)}")
                raise
        return self._client

# Global instance
db = DatabaseConfig()
