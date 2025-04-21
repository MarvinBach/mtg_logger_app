from typing import List, Dict, Any, Optional
from config.config import config

class DataProvider:
    """Provides data for visualization"""
    @staticmethod
    def get_players() -> List[Dict[str, Any]]:
        response = config.db.table("players").select("*").execute()
        return response.data

    @staticmethod
    def get_player_by_id(player_id: int) -> Optional[str]:
        response = (
            config.db.table("players")
            .select("name")
            .eq("id", player_id)
            .limit(1)
            .execute()
        )
        return response.data[0]["name"] if response.data else None

    @staticmethod
    def get_recent_games(limit: Optional[int] = None) -> List[Dict[str, Any]]:
        query = config.db.table("games").select("*").order("played_at", desc=True)
        if limit is not None:
            query = query.limit(limit)
        return query.execute().data

    @staticmethod
    def get_player_games(player_id: int) -> List[Dict[str, Any]]:
        return config.db.table("games").select("*").or_(
            f"winner_id.eq.{player_id},loser_id.eq.{player_id}"
        ).execute().data
