import streamlit as st
from datetime import datetime
from data.repositories import GameRepository, PlayerRepository

def render_game_history(limit: int = 5) -> None:
    """Render recent game history"""
    st.header("Game History")

    games = GameRepository.get_recent(limit=limit)
    for game in games:
        winner_name = PlayerRepository.get_by_id(game["winner_id"])
        loser_name = PlayerRepository.get_by_id(game["loser_id"])

        # Handle date display
        played_at_str = ""
        if game["played_at"]:
            if isinstance(game["played_at"], str):
                played_at = datetime.fromisoformat(game["played_at"]).date()
            else:
                played_at = game["played_at"].date()
            played_at_str = f" on {played_at}"

        st.write(
            f"{winner_name} defeated {loser_name} in {game['format']} format{played_at_str}"
        )
