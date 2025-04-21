from typing import List, Dict, Any, Optional
from data.repositories import PlayerRepository, GameRepository

class DataProvider:
    """Provides data for visualization"""
    @staticmethod
    def get_players() -> List[Dict[str, Any]]:
        return PlayerRepository.get_all()

    @staticmethod
    def get_player_by_id(player_id: int) -> Optional[str]:
        return PlayerRepository.get_by_id(player_id)

    @staticmethod
    def get_recent_games(limit: Optional[int] = None) -> List[Dict[str, Any]]:
        return GameRepository.get_recent(limit)

    @staticmethod
    def get_player_games(player_id: int) -> List[Dict[str, Any]]:
        return GameRepository.get_by_player(player_id)
