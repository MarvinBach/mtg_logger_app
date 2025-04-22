import streamlit as st
from supabase import create_client
from typing import Optional
import logging
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class Config:
    """Central configuration class"""
    _instance: Optional['Config'] = None
    _db_client = None
    _logger = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._setup_logging()
        return cls._instance

    def _setup_logging(self):
        if self._logger is None:
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            self._logger = logging.getLogger('mtg_logger')

    @property
    def logger(self):
        if self._logger is None:
            self._setup_logging()
        return self._logger

    @property
    def db(self):
        if self._db_client is None:
            try:
                # Try to get from streamlit secrets first, fall back to env vars
                url = st.secrets.get("SUPABASE_URL", os.getenv("SUPABASE_URL"))
                key = st.secrets.get("SUPABASE_KEY", os.getenv("SUPABASE_KEY"))

                if not url or not key:
                    raise ValueError("Supabase credentials not found in secrets or .env file")

                self._db_client = create_client(url, key)

            except Exception as e:
                self.logger.error(f"Database connection failed: {str(e)}")
                raise
        return self._db_client

# Create the singleton instance
config = Config()
