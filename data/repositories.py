from typing import List, Dict, Any, Optional
from config.config import config
from core.models import Player, Game

class PlayerRepository:
    """Repository for player-related database operations"""
    @staticmethod
    def add(name: str) -> Dict[str, Any]:
        player = Player(name=name)
        player.validate()

        config.logger.info(f"Adding new player: {name}")
        response = config.db.table("players").insert({"name": name.strip()}).execute()

        if not response.data:
            raise Exception("Failed to add player to database")
        return response.data[0]

    @staticmethod
    def delete(player_id: int) -> None:
        config.logger.info(f"Deleting player with ID: {player_id}")
        response = config.db.table("players").delete().eq("id", player_id).execute()
        if not response.data:
            raise Exception(f"Failed to delete player with ID {player_id}")

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        response = config.db.table("players").select("*").execute()
        return response.data

    @staticmethod
    def get_by_id(player_id: int) -> Optional[str]:
        response = (
            config.db.table("players")
            .select("name")
            .eq("id", player_id)
            .limit(1)
            .execute()
        )
        return response.data[0]["name"] if response.data else None


class GameRepository:
    """Repository for game-related database operations"""
    @staticmethod
    def add(game: Game) -> Dict[str, Any]:
        game.validate()
        config.logger.info(f"Adding new game: {game}")

        response = config.db.table("games").insert(game.to_dict()).execute()
        if not response.data:
            raise Exception("Failed to add game to database")
        return response.data[0]

    @staticmethod
    def delete(game_id: int) -> None:
        config.logger.info(f"Deleting game with ID: {game_id}")
        response = config.db.table("games").delete().eq("id", game_id).execute()
        if not response.data:
            raise Exception(f"Failed to delete game with ID {game_id}")

    @staticmethod
    def get_recent(limit: Optional[int] = None) -> List[Dict[str, Any]]:
        query = config.db.table("games").select("*").order("played_at", desc=True)
        if limit is not None:
            query = query.limit(limit)
        return query.execute().data

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        return config.db.table("games").select("*").execute().data

    @staticmethod
    def get_by_player(player_id: int) -> List[Dict[str, Any]]:
        return config.db.table("games").select("*").or_(
            f"winner_id.eq.{player_id},loser_id.eq.{player_id}"
        ).execute().data
