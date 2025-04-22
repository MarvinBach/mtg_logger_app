from typing import List, Dict, Any, Optional
import streamlit as st
from config.config import config

class DataProvider:
    """Provides data for visualization"""

    @st.cache_data(ttl=60)  # Cache for 1 minute
    def get_games(_self) -> List[Dict[str, Any]]:
        """Get all games"""
        return config.db.table("games").select("*").execute().data

    @st.cache_data(ttl=60)  # Cache for 1 minute
    def get_recent_games(_self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent games with limit"""
        query = config.db.table("games").select("*").order("played_at", desc=True)
        if limit is not None:
            query = query.limit(limit)
        return query.execute().data

    @st.cache_data(ttl=60)  # Cache for 1 minute
    def get_players(_self) -> List[Dict[str, Any]]:
        """Get all players"""
        return config.db.table("players").select("*").execute().data

    @st.cache_data(ttl=60)  # Cache for 1 minute
    def get_player_by_id(_self, player_id: int) -> Optional[str]:
        """Get player name by ID"""
        response = config.db.table("players").select("name").eq("id", player_id).limit(1).execute()
        return response.data[0]["name"] if response.data else None

    @staticmethod
    @st.cache_data(ttl=60)  # Cache for 1 minute
    def get_player_games(player_id: int) -> List[Dict[str, Any]]:
        return config.db.table("games").select("*").or_(
            f"winner_id.eq.{player_id},loser_id.eq.{player_id}"
        ).execute().data
