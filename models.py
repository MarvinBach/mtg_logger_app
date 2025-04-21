from typing import List, Dict, Any, Optional
import streamlit as st
from config import db

class Player:
    def __init__(self, id: Optional[int] = None, name: Optional[str] = None):
        self.id = id
        self.name = name

    def add(self) -> Dict[str, Any]:
        """Add a new player to the database"""
        data = {"name": self.name}
        response = db.client.table("players").insert(data).execute()
        return response

    @classmethod
    def delete(cls, player_id: int) -> Dict[str, Any]:
        """Delete a player from the database by ID"""
        response = db.client.table("players").delete().eq("id", player_id).execute()
        return response

    @classmethod
    def get_all(cls) -> List[Dict[str, Any]]:
        """Get all players from the database."""
        response = db.client.table("players").select("*").execute()
        return response.data

    @classmethod
    def get_by_id(cls, player_id: int) -> str:
        """Get player name by ID"""
        response = (
            db.client.table("players")
            .select("name")
            .eq("id", player_id)
            .limit(1)
            .execute()
        )
        if response.data:
            return response.data[0]["name"]
        return "Unknown"


class Game:
    def __init__(
        self,
        winner_id: int,
        loser_id: int,
        game_format: str,
        edition: Optional[str],
        winner_colors: List[str],
        loser_colors: List[str],
        game_id: Optional[int] = None,
    ):
        self.id = game_id
        self.winner_id = winner_id
        self.loser_id = loser_id
        self.game_format = game_format
        self.edition = edition
        self.winner_colors = winner_colors
        self.loser_colors = loser_colors

    def add(self) -> Dict[str, Any]:
        """Add a new game to the database"""
        data = {
            "winner_id": self.winner_id,
            "loser_id": self.loser_id,
            "format": self.game_format,
            "edition": self.edition,
            "winner_colors": self.winner_colors,
            "loser_colors": self.loser_colors,
        }
        response = db.client.table("games").insert(data).execute()
        return response

    @classmethod
    def delete(cls, game_id: int) -> str:
        """Delete a game from the database by ID"""
        response = db.client.table("games").delete().eq("id", game_id).execute()
        if response.status_code == 200:
            return f"Game with ID {game_id} deleted successfully."
        else:
            return f"Failed to delete the game with ID {game_id}. Error: {response.error_message}"

    @classmethod
    def get_recent(cls, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get recent games from the database"""
        query = db.client.table("games").select("*").order("played_at", desc=True)
        if limit is not None:
            query = query.limit(limit)
        return query.execute().data

    @classmethod
    def get_all(cls) -> List[Dict[str, Any]]:
        """Get all games from the database."""
        response = db.client.table("games").select("*").execute()
        return response.data

    @staticmethod
    def get_all_by_player(player_id: int) -> List[Dict[str, Any]]:
        """Get all games by player from the database"""
        response = db.client.table("games").select("*").or_(
            f"winner_id.eq.{player_id},loser_id.eq.{player_id}"
        ).execute()
        return response.data
