import streamlit as st
from visualization import DataProvider, StatsCalculator, DataVisualizer
from ui.components.game_form import render_game_form
from ui.components.history_view import render_game_history
from data.repositories import PlayerRepository
from core.enums import Edition, GameFormat

st.title("Magic The Gathering Game Logger")

# Initialize visualization components
data_provider = DataProvider()
stats_calculator = StatsCalculator(data_provider)
visualizer = DataVisualizer(stats_calculator)

# Render game form
render_game_form()

# Render game history with its own filters
render_game_history()

# Player statistics section
st.header("Player Statistics")

# Overall win rates (show all games as default)
overall_start_date = st.date_input(
                "Stats From Date",
                value=None,
                key="overall_start_date",
                help="Start date for player statistics (inclusive)"
            )
overall_end_date = st.date_input(
                "Stats To Date",
                value=None,
                key="overall_end_date",
                help="End date for player statistics (inclusive)"
            )
overall_edition_filter = st.selectbox(
                "Stats Edition",
                ["All"] + Edition.list()[1:],
                key="overall_edition_filter"
            )
overall_format_filter = st.selectbox(
                "Stats Format",
                ["All"] + GameFormat.list(),  # Include all formats
                key="overall_format_filter"
            )
visualizer.plot_player_win_rates(start_date=overall_start_date, end_date=overall_end_date, edition_filter=overall_edition_filter, format_filter=overall_format_filter)

# Player details with separate filters
players = PlayerRepository.get_all()
player_names = sorted([p["name"] for p in players])  # Sort player names alphabetically

if player_names:
    st.subheader("Player Details")

    # Player selection and filters in two rows
    col1, col2 = st.columns(2)

    with col1:
        selected_player = st.selectbox(
            "Select a player",
            player_names,
            key="stats_player_select"
        )

    # Filters in a separate container for visual separation
    with st.container():
        filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

        with filter_col1:
            stats_start_date = st.date_input(
                "Stats From Date",
                value=None,
                key="stats_start_date",
                help="Start date for player statistics (inclusive)"
            )

        with filter_col2:
            stats_end_date = st.date_input(
                "Stats To Date",
                value=None,
                key="stats_end_date",
                help="End date for player statistics (inclusive)"
            )

        with filter_col3:
            stats_edition = st.selectbox(
                "Stats Edition",
                ["All"] + Edition.list()[1:],
                key="stats_edition"
            )

        with filter_col4:
            stats_format = st.selectbox(
                "Stats Format",
                ["All"] + GameFormat.list(),  # Include all formats
                key="stats_format"
            )

    # Show filtered player statistics
    if selected_player:
        visualizer.plot_player_matchups(
            selected_player,
            start_date=stats_start_date,
            end_date=stats_end_date,
            edition_filter=stats_edition,
            format_filter=stats_format
        )

        visualizer.plot_player_win_rates_by_color(
            selected_player,
            start_date=stats_start_date,
            end_date=stats_end_date,
            edition_filter=stats_edition,
            format_filter=stats_format
        )

        visualizer.plot_player_individual_color_stats(
            selected_player,
            start_date=stats_start_date,
            end_date=stats_end_date,
            edition_filter=stats_edition,
            format_filter=stats_format
        )

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
