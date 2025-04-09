import streamlit as st
import pandas as pd
from datetime import datetime

from constants import EDITION_OPTIONS, COLOR_OPTIONS, FORMAT_OPTIONS
from models import Player, Game
from plot import WinRatePlotter, plot_head_to_head_win_rates


st.title("Magic The Gathering Game Logger")

# --- Add Game Result ---
st.header("Add game result")
players = Player.get_all()
player_map = {p["name"]: p["id"] for p in players}
player_names = list(player_map.keys())

if not player_names:
    st.warning("Add some players first!")
else:
    winner = st.selectbox("Winner", player_names, key="winner")
    loser = st.selectbox("Loser", player_names, key="loser")
    game_format = st.selectbox(
        "Format", ["Draft", "Sealed", "Cube Draft", "Constructed", "Commander", "Arena"]
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
            edition_to_submit = selected_edition if selected_edition != "None" else None
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

# --- Game History ---
st.header("Game History")
games = Game.get_recent(limit=5)
for g in games:
    winner_name = Player.get_by_id(g["winner_id"])
    loser_name = Player.get_by_id(g["loser_id"])

    if isinstance(g["played_at"], str):
        played_at = datetime.fromisoformat(g["played_at"]).date()
    else:
        played_at = g["played_at"].date()

    st.write(
        f"{winner_name} defeated {loser_name} in {g['format']} format on {played_at}"
    )

# --- Player Win Rates ---
st.header("Player Win Rates")
plotter = WinRatePlotter()
plotter.plot_player_win_rates()

# --- Player Match History ---
st.header("Player Match History")
history_player_name = st.selectbox(
    "Select a player to view history", player_names, key="history_player"
)
history_format = st.selectbox(
    "Filter by Format", ["All"] + FORMAT_OPTIONS, key="history_format"
)
history_edition = st.selectbox(
    "Filter by Edition", ["All"] + EDITION_OPTIONS, key="history_edition"
)
history_player_id = player_map[history_player_name]
player_games = Game.get_all_by_player(history_player_id)

if history_format != "All":
    player_games = [g for g in player_games if g["format"] == history_format]

if history_edition != "All":
    player_games = [g for g in player_games if g.get("edition") == history_edition]

# --- Head-to-Head Win Rates ---
st.subheader(f"Head-to-Head Win Rates for {history_player_name}")
plot_head_to_head_win_rates(history_player_name, history_format, history_edition)

# --- Player Win Rate by Color ---
st.subheader(f"Win Rates for {history_player_name} by Color")
plotter.plot_player_win_rates_by_color(
    history_player_name, history_format, history_edition
)

# --- Add New Player ---
st.header("Add new player")
new_player = st.text_input("Player name")
if st.button("Add Player"):
    if not new_player.strip():
        st.error("Player name cannot be empty.")
    else:
        try:
            Player.add(name=new_player)
            st.success(f"Player {new_player} added successfully!")
        except Exception as e:
            st.error(f"Failed to add player: {e}")
