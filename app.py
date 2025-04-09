import streamlit as st
import pandas as pd
from datetime import datetime

from constants import EDITION_OPTIONS, COLOR_OPTIONS, FORMAT_OPTIONS
from db import add_game
from models import Player, Game
from plot import WinRatePlotter


st.title("Magic The Gathering Game Logger")

# --- Add Game Result ---
st.header("Add game result")
add_game()

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
opponent_stats = {}

for g in player_games:
    opponent_id = (
        g["loser_id"] if g["winner_id"] == history_player_id else g["winner_id"]
    )
    opponent_name = Player.get_by_id(opponent_id)

    if opponent_name not in opponent_stats:
        opponent_stats[opponent_name] = {"wins": 0, "losses": 0}

    if g["winner_id"] == history_player_id:
        opponent_stats[opponent_name]["wins"] += 1
    else:
        opponent_stats[opponent_name]["losses"] += 1

summary_data = []
for opponent, record in opponent_stats.items():
    wins = record["wins"]
    losses = record["losses"]
    total = wins + losses
    win_rate = f"{(wins / total) * 100:.0f}%" if total > 0 else "—"
    summary_data.append(
        {
            "Opponent": opponent,
            "Wins": wins,
            "Losses": losses,
            "Win Rate": win_rate,
        }
    )

if summary_data:
    summary_df = pd.DataFrame(summary_data).sort_values(by="Wins", ascending=False)
    st.dataframe(summary_df, use_container_width=True)
else:
    st.write("No head-to-head data available.")

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
