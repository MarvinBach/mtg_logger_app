import streamlit as st
from datetime import datetime, timedelta
from data.repositories import GameRepository, PlayerRepository
from core.enums import Edition
from .edit_game_form import edit_game_modal

def get_game_date(game):
    """Extract date from game's played_at field"""
    try:
        if not game.get("played_at"):
            return None

        if isinstance(game["played_at"], str):
            return datetime.fromisoformat(game["played_at"]).date()
        return game["played_at"].date()
    except (ValueError, AttributeError):
        return None

def filter_games(games, start_date, end_date, edition_filter, player_filter, player_map):
    """Filter games based on selected criteria"""
    filtered_games = games

    # Filter by date range
    if start_date or end_date:
        filtered_games = []
        for game in games:
            game_date = get_game_date(game)
            if not game_date:
                continue

            if start_date and end_date:
                if start_date <= game_date <= end_date:
                    filtered_games.append(game)
            elif start_date:
                if game_date >= start_date:
                    filtered_games.append(game)
            elif end_date:
                if game_date <= end_date:
                    filtered_games.append(game)

    if edition_filter != "All":
        filtered_games = [g for g in filtered_games if g.get("edition") == edition_filter]

    if player_filter != "All":
        player_id = player_map[player_filter]
        filtered_games = [
            g for g in filtered_games
            if g["winner_id"] == player_id or g["loser_id"] == player_id
        ]

    return filtered_games

def render_game_history(limit: int = 5) -> None:
    """Render recent game history"""
    st.header("Game History")

    # Get all data
    players = PlayerRepository.get_all()
    player_map = {p["name"]: p["id"] for p in players}

    # Filter and display options
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 0.7])

    with col1:
        start_date = st.date_input(
            "From Date",
            value=None,
            key="history_start_date",
            help="Start date (inclusive)"
        )

    with col2:
        end_date = st.date_input(
            "To Date",
            value=None,
            key="history_end_date",
            help="End date (inclusive)"
        )

    with col3:
        edition_filter = st.selectbox(
            "Edition",
            ["All"] + Edition.list()[1:],
            key="history_edition_filter"
        )

    with col4:
        player_filter = st.selectbox(
            "Player",
            ["All"] + list(player_map.keys()),
            key="history_player_filter"
        )

    with col5:
        display_limit = st.number_input(
            "Show games",
            min_value=1,
            max_value=100,
            value=5,
            step=5,
            key="history_limit"
        )

    # Get filtered games with selected limit
    games = GameRepository.get_recent(limit=display_limit)
    filtered_games = filter_games(games, start_date, end_date, edition_filter, player_filter, player_map)

    if not filtered_games:
        st.info("No games found matching the selected filters.")
        return

    # Display filtered games
    st.caption(f"Showing {len(filtered_games)} games")
    for game in filtered_games:
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
