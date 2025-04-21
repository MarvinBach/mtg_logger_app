import streamlit as st
from datetime import datetime
from data.repositories import GameRepository, PlayerRepository
from .edit_game_form import edit_game_modal

def render_game_history(limit: int = 5) -> None:
    """Render recent game history"""
    st.header("Game History")

    games = GameRepository.get_recent(limit=limit)
    for game in games:
        # Create columns for game info and edit button
        col1, col2 = st.columns([0.85, 0.15])

        with col1:
            winner_name = PlayerRepository.get_by_id(game["winner_id"])
            loser_name = PlayerRepository.get_by_id(game["loser_id"])

            # Handle date display
            played_at_str = ""
            if game.get("played_at"):
                try:
                    if isinstance(game["played_at"], str):
                        played_at = datetime.fromisoformat(game["played_at"])
                    else:
                        played_at = game["played_at"]
                    played_at_str = f" on {played_at.strftime('%Y-%m-%d %H:%M')}"
                except (ValueError, AttributeError) as e:
                    st.error(f"Error parsing date: {e}")

            # Display game info with colors
            winner_colors = ", ".join(game.get("winner_colors", []))
            loser_colors = ", ".join(game.get("loser_colors", []))

            game_info = (
                f"{winner_name} ({winner_colors}) defeated "
                f"{loser_name} ({loser_colors}) in {game['format']} format{played_at_str}"
            )

            st.write(game_info)

        with col2:
            edit_game_modal(game)
