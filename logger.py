import streamlit as st

from models import Player, Game
from constants import EDITION_OPTIONS, COLOR_OPTIONS


def add_game(player_map, player_names) -> None:
    if not player_names:
        st.warning("Add some players first!")
    else:
        winner = st.selectbox("Winner", player_names, key="winner")
        loser = st.selectbox("Loser", player_names, key="loser")
        game_format = st.selectbox(
            "Format",
            ["Draft", "Sealed", "Cube Draft", "Constructed", "Commander", "Arena"],
        )
        selected_edition = st.selectbox(
            "Edition (optional)", options=["None"] + EDITION_OPTIONS, index=0
        )
        winner_colors = st.multiselect(
            "Winner's Colors (optional)", options=COLOR_OPTIONS, default=[]
        )
        loser_colors = st.multiselect(
            "Loser's Colors (optional)", options=COLOR_OPTIONS, default=[]
        )

        if st.button("Add Game Result"):
            if winner == loser:
                st.error("Winner and loser cannot be the same player.")
            else:
                edition_to_submit = (
                    selected_edition if selected_edition != "None" else None
                )
                try:
                    Game(
                        winner_id=player_map[winner],
                        loser_id=player_map[loser],
                        game_format=game_format,
                        edition=edition_to_submit,
                        winner_colors=winner_colors,
                        loser_colors=loser_colors,
                    ).add()
                    st.success(
                        f"Game result added: {winner} defeated {loser} in {game_format} format!"
                    )
                except Exception as e:
                    st.error(f"Failed to add game: {e}")
