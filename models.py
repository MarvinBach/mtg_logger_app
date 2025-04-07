import streamlit as st
from supabase import create_client

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

class Player:
    def __init__(self, id: int = None, name: str = None):
        self.id = id
        self.name = name

    def add(self):
        """Add a new player to the database"""
        data = {"name": self.name}
        response = supabase.table("players").insert(data).execute()
        return response

    @classmethod
    def delete(cls, player_id: int):
        """Delete a player from the database by ID"""
        response = supabase.table("players").delete().eq("id", player_id).execute()
        return response

    @classmethod
    def get_all(cls):
        """Get all players from the database."""
        response = supabase.table("players").select("*").execute()
        return response.data

    @classmethod
    def get_by_id(cls, player_id: int):
        """Get player name by ID"""
        response = supabase.table("players").select("name").eq("id", player_id).limit(1).execute()
        if response.data:
            return response.data[0]["name"]
        return "Unknown"

class Game:
    def __init__(self, winner_id, loser_id, game_format, edition, winner_colors, loser_colors, game_id=None):
        self.id = game_id
        self.winner_id = winner_id
        self.loser_id = loser_id
        self.game_format = game_format
        self.edition = edition
        self.winner_colors = winner_colors
        self.loser_colors = loser_colors

    def add(self):
        """Add a new game to the database"""
        data = {
            "winner_id": self.winner_id,
            "loser_id": self.loser_id,
            "format": self.game_format,
            "edition": self.edition,
            "winner_colors": self.winner_colors,
            "loser_colors": self.loser_colors
        }
        response = supabase.table("games").insert(data).execute()
        return response

    @classmethod
    def delete(cls, game_id: int):
        """Delete a game from the database by ID"""
        response = supabase.table("games").delete().eq("id", game_id).execute()
        if response.status_code == 200:
            return f"Game with ID {game_id} deleted successfully."
        else:
            return f"Failed to delete the game with ID {game_id}. Error: {response.error_message}"

    @classmethod
    def get_recent(cls, limit=None):
        """Get recent games from the database"""
        query = supabase.table("games").select("*").order("played_at", desc=True)
        if limit is not None:
            query = query.limit(limit)
        return query.execute().data
