from typing import List, Dict, Any, Optional
import streamlit as st
from config.config import config
from data.repositories import GameRepository, PlayerRepository

class DataProvider:
    """Provides data for visualization"""

    @st.cache_data(ttl=60)  # Cache for 1 minute
    def get_games(_self) -> List[Dict[str, Any]]:
        """Get all games"""
        return GameRepository.get_all()

    @st.cache_data(ttl=60)  # Cache for 1 minute
    def get_recent_games(_self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent games with limit"""
        return GameRepository.get_recent(limit=limit)

    @st.cache_data(ttl=60)  # Cache for 1 minute
    def get_players(_self) -> List[Dict[str, Any]]:
        """Get all players"""
        return PlayerRepository.get_all()

    @st.cache_data(ttl=60)  # Cache for 1 minute
    def get_player_by_id(_self, player_id: int) -> str:
        """Get player name by ID"""
        return PlayerRepository.get_by_id(player_id)

    @staticmethod
    @st.cache_data(ttl=60)  # Cache for 1 minute
    def get_player_games(player_id: int) -> List[Dict[str, Any]]:
        return config.db.table("games").select("*").or_(
            f"winner_id.eq.{player_id},loser_id.eq.{player_id}"
        ).execute().data
