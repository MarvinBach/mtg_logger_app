import streamlit as st
from typing import List, Dict
from core.enums import GameFormat, Color, Edition
from core.models import Game
from data.repositories import GameRepository, PlayerRepository
from datetime import datetime

def render_game_form() -> None:
    """Render the game input form"""
    st.header("Add game result")

    # Get players
    players = PlayerRepository.get_all()
    player_map = {p["name"]: p["id"] for p in players}
    player_names = list(player_map.keys())

    if not player_names:
        st.warning("Add some players first!")
        return

    # Form inputs
    winner = st.selectbox("Winner", player_names, key="winner")
    loser = st.selectbox("Loser", player_names, key="loser")
    game_format = st.selectbox("Format", GameFormat.list())

    selected_edition = st.selectbox(
        "Edition (optional)",
        options=["None"] + Edition.list()[1:],
        index=0
    )

    winner_colors = st.multiselect(
        "Winner's Colors (optional)",
        options=Color.list(),
        default=[]
    )

    loser_colors = st.multiselect(
        "Loser's Colors (optional)",
        options=Color.list(),
        default=[]
    )

    if st.button("Add Game Result"):
        if winner == loser:
            st.error("Winner and loser cannot be the same player.")
            return

        try:
            game = Game(
                winner_id=player_map[winner],
                loser_id=player_map[loser],
                game_format=GameFormat(game_format),
                winner_colors=[Color(c) for c in winner_colors],
                loser_colors=[Color(c) for c in loser_colors],
                edition=Edition(selected_edition) if selected_edition != "None" else None,
                played_at=datetime.now()  # Set current date and time
            )
            GameRepository.add(game)
            st.success(
                f"Game result added: {winner} defeated {loser} in {game_format} format!"
            )
        except Exception as e:
            st.error(f"Failed to add game: {e}")
