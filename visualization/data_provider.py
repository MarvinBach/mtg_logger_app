from typing import List, Dict, Any, Optional
from config.config import config
from data.repositories import GameRepository, PlayerRepository

class DataProvider:
    """Provides data for visualization"""
    def get_games(self) -> List[Dict[str, Any]]:
        """Get all games"""
        return GameRepository.get_all()

    def get_recent_games(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent games with limit"""
        return GameRepository.get_recent(limit=limit)

    def get_players(self) -> List[Dict[str, Any]]:
        """Get all players"""
        return PlayerRepository.get_all()

    def get_player_by_id(self, player_id: int) -> str:
        """Get player name by ID"""
        return PlayerRepository.get_by_id(player_id)

    @staticmethod
    def get_player_games(player_id: int) -> List[Dict[str, Any]]:
        return config.db.table("games").select("*").or_(
            f"winner_id.eq.{player_id},loser_id.eq.{player_id}"
        ).execute().data
