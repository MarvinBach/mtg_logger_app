import streamlit as st
from visualization.data_provider import DataProvider
from visualization.stats_calculator import StatsCalculator
from visualization.visualizer import DataVisualizer
from ui.components.game_form import render_game_form
from ui.components.history_view import render_game_history
from data.repositories import PlayerRepository

st.title("Magic The Gathering Game Logger")

# Initialize visualization components
data_provider = DataProvider()
stats_calculator = StatsCalculator(data_provider)
visualizer = DataVisualizer(stats_calculator)

# Render game form
render_game_form()

# Render game history
render_game_history(limit=5)

# Player statistics
st.header("Player Statistics")
visualizer.plot_player_win_rates()

# Player details
players = PlayerRepository.get_all()
player_names = [p["name"] for p in players]

if player_names:
    selected_player = st.selectbox(
        "Select a player to view details",
        player_names,
        key="player_details"
    )

    # Show player statistics
    visualizer.plot_player_matchups(selected_player)
    visualizer.plot_player_win_rates_by_color(selected_player)

# Add new player
st.header("Add new player")
new_player_name = st.text_input("Player name")
if st.button("Add Player"):
    try:
        PlayerRepository.add(new_player_name)
        st.success(f"Player {new_player_name} added successfully!")
    except ValueError as ve:
        st.error(str(ve))
    except Exception as e:
        st.error(f"Failed to add player: {e}")
